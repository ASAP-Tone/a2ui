/*
 Copyright 2025 Google LLC

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      https://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
 */

import { Part, SendMessageSuccessResponse, Task } from "@a2a-js/sdk";
import { A2AClient } from "@a2a-js/sdk/client";
import { v0_8 } from "@a2ui/lit";

const A2AUI_MIME_TYPE = "application/json+a2aui";

export class A2UIClient {
  #serverUrl: string;
  #client: A2AClient | null = null;

  constructor(serverUrl: string = "") {
    this.#serverUrl = serverUrl;
  }

  #ready: Promise<void> = Promise.resolve();
  get ready() {
    return this.#ready;
  }

  async #getClient() {
    if (!this.#client) {
      // Default to Cloud Run orchestrator if no URL provided
      const baseUrl = this.#serverUrl || "https://adk-orchestrator-service-39067166180.us-central1.run.app";
      this.#client = await A2AClient.fromCardUrl(
        `${baseUrl}/.well-known/agent-card.json`,
        {
          fetchImpl: async (url, init) => {
            const headers = new Headers(init?.headers);
            headers.set("X-A2A-Extensions", "https://a2ui.org/a2a-extension/a2ui/v0.8");
            return fetch(url, { ...init, headers });
          }
        }
      );
    }
    return this.#client;
  }

  async send(
    message: v0_8.Types.A2UIClientEventMessage | string
  ): Promise<v0_8.Types.ServerToClientMessage[]> {
    const client = await this.#getClient();

    let parts: Part[] = [];

    if (typeof message === 'string') {
      // Try to parse as JSON first, just in case
      try {
        const parsed = JSON.parse(message);
        if (typeof parsed === 'object' && parsed !== null) {
          parts = [{
            kind: "data",
            data: parsed as unknown as Record<string, unknown>,
            mimeType: A2AUI_MIME_TYPE,
          } as Part];
        } else {
          parts = [{ kind: "text", text: message }];
        }
      } catch {
        parts = [{ kind: "text", text: message }];
      }
    } else {
      parts = [{
        kind: "data",
        data: message as unknown as Record<string, unknown>,
        mimeType: A2AUI_MIME_TYPE,
      } as Part];
    }

    const response = await client.sendMessage({
      message: {
        messageId: crypto.randomUUID(),
        role: "user",
        parts: parts,
        kind: "message",
      },
    });

    console.log("A2A Raw Response:", response);

    if ("error" in response) {
      console.error("A2A Error Response:", response.error);
      throw new Error(response.error.message);
    }

    let task = (response as SendMessageSuccessResponse).result as Task;
    console.log("Initial Task:", task);

    // Polling for completion
    let attempts = 0;
    while (task.kind === 'task' && (task.status?.state === 'working' || !task.status?.message) && attempts < 3) {
        console.log(`Task state: ${task.status?.state}, Message present: ${!!task.status?.message}. Polling... (${attempts + 1})`);
        await new Promise(resolve => setTimeout(resolve, 1000));
        try {
            const updateResponse = await client.getTask({ id: task.id });
            if ('error' in updateResponse) {
                 console.warn("Error polling task:", updateResponse.error);
                 break;
            }
            task = updateResponse.result as Task;
        } catch (e) {
            console.error("Polling exception:", e);
            break;
        }
        attempts++;
    }
    console.log( "Polled attempts:", attempts);
    console.log("Final Task State:", task);

    let messageParts = task.status?.message?.parts;
    
    // Fallback 1: Check events history
    if (!messageParts && (task as any).events && (task as any).events.length > 0) {
        const events = (task as any).events;
        for (let i = events.length - 1; i >= 0; i--) {
            if (events[i].status?.message?.parts) {
                console.log("Found message parts in task history events!");
                messageParts = events[i].status.message.parts;
                break;
            }
        }
    }

    // Fallback 2: Check artifacts (common in ADK orchestrator responses)
    if (!messageParts && (task as any).artifacts && (task as any).artifacts.length > 0) {
         console.log("Found artifacts in task, checking for parts...");
         const artifacts = (task as any).artifacts;
         // Artifacts usually contain parts directly or nested
         for (const artifact of artifacts) {
             if (artifact.parts && artifact.parts.length > 0) {
                 console.log("Found parts in artifact:", artifact.artifactId);
                 // We accumulate parts or just take the first valid one? 
                 // Usually artifacts represent the 'response' content.
                 // We will append them to a list if we are building a message.
                 // But here we need 'messageParts' structure.
                 // Let's assume the artifact parts ARE the message parts we need.
                 if (!messageParts) messageParts = [];
                 messageParts.push(...artifact.parts);
             }
         }
    }

    if (task.kind === "task" && messageParts) {
      const messages: v0_8.Types.ServerToClientMessage[] = [];
      console.log(`Processing ${messageParts.length} parts...`);
      
      for (const part of messageParts) {
        console.log("Processing part:", part);
        if (part.kind === 'data') {
          console.log("Found data part, adding to A2UI messages:", part.data);
          messages.push(part.data as v0_8.Types.ServerToClientMessage);
        } else {
          console.log(`Skipping part of kind: ${part.kind}`);
        }
      }
      return messages;
    }

    console.warn("A2A Response (after polling) did not contain a valid task with message parts.");
    return [];
  }
}
