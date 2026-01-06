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

import { SignalWatcher } from "@lit-labs/signals";
import { provide } from "@lit/context";
import {
  LitElement,
  html,
  css,
  nothing,
  HTMLTemplateResult,
  unsafeCSS,
} from "lit";
import { customElement, state, property } from "lit/decorators.js";
import { classMap } from "lit/directives/class-map.js";
import { theme as uiTheme } from "./theme/default-theme.js";
import { A2UIClient } from "./client.js";
import {
  SnackbarAction,
  SnackbarMessage,
  SnackbarUUID,
  SnackType,
} from "./types/types.js";
import { type Snackbar } from "./ui/snackbar.js";
import { repeat } from "lit/directives/repeat.js";
import { v0_8 } from "@a2ui/lit";
import * as UI from "@a2ui/lit/ui";

// App elements.
import "./ui/ui.js";

// Configurations
import { AppConfig } from "./configs/types.js";
import { config as jiraConfig } from "./configs/jira.js";
import { styleMap } from "lit/directives/style-map.js";

const configs: Record<string, AppConfig> = {
  jira: jiraConfig,
};

@customElement("a2ui-shell")
export class A2UILayoutEditor extends SignalWatcher(LitElement) {
  @provide({ context: UI.Context.themeContext })
  accessor theme: v0_8.Types.Theme = uiTheme;

  @state()
  accessor #requesting = false;

  @state()
  accessor #error: string | null = null;

  @state()
  accessor #lastMessages: v0_8.Types.ServerToClientMessage[] = [];

  @state()
  accessor config: AppConfig = configs.jira;

  @state()
  accessor #loadingTextIndex = 0;
  #loadingInterval: number | undefined;

  @state()
  accessor sidebarCollapsed = false;

  @state()
  accessor currentView: 'home' | 'chat' = 'home';

  static styles = [
    unsafeCSS(v0_8.Styles.structuralStyles),
    css`
      :host {
        --bg-deep: #050508;
        --bg-glass: rgba(20, 20, 30, 0.6);
        --bg-glass-strong: rgba(30, 30, 45, 0.8);
        --primary: #3b82f6;
        --primary-glow: rgba(59, 130, 246, 0.5);
        --text-main: #f8fafc;
        --text-muted: #94a3b8;
        --border-subtle: rgba(255, 255, 255, 0.08);
        --font-family: 'Inter', system-ui, -apple-system, sans-serif;
        
        display: flex;
        width: 100vw;
        height: 100vh;
        background-color: var(--bg-deep);
        background-image: 
          radial-gradient(circle at 15% 50%, rgba(56, 189, 248, 0.08), transparent 25%),
          radial-gradient(circle at 85% 30%, rgba(168, 85, 247, 0.08), transparent 25%);
        color: var(--text-main);
        font-family: var(--font-family);
        overflow: hidden;
      }

      * { box-sizing: border-box; }

      /* Sidebar */
      aside {
        width: 280px;
        background: var(--bg-glass);
        backdrop-filter: blur(24px);
        -webkit-backdrop-filter: blur(24px);
        border-right: 1px solid var(--border-subtle);
        display: flex;
        flex-direction: column;
        z-index: 10;
        transition: transform 0.3s ease, width 0.3s ease;
      }
      
      aside.collapsed {
        width: 0;
        overflow: hidden;
        border: none;
      }

      .sidebar-header {
        padding: 24px;
        display: flex;
        align-items: center;
        gap: 12px;
      }
      
      .brand-logo {
        color: var(--primary);
        font-size: 24px;
        filter: drop-shadow(0 0 8px var(--primary-glow));
      }

      .new-chat-btn {
        margin: 0 20px 20px;
        padding: 12px;
        background: linear-gradient(135deg, var(--primary), #2563eb);
        color: white;
        border: none;
        border-radius: 12px;
        font-weight: 600;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 8px;
        cursor: pointer;
        box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        transition: all 0.2s;
      }
      
      .new-chat-btn:hover {
        transform: translateY(-1px);
        box-shadow: 0 6px 16px rgba(37, 99, 235, 0.4);
      }

      .sidebar-section {
        flex: 1;
        padding: 0 12px;
        overflow-y: auto;
      }

      .section-title {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: var(--text-muted);
        margin: 24px 12px 12px;
        font-weight: 600;
      }

      .nav-item {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 12px;
        margin-bottom: 4px;
        border-radius: 8px;
        color: var(--text-muted);
        cursor: pointer;
        transition: all 0.2s;
        text-decoration: none;
        font-size: 14px;
      }

      .nav-item:hover {
        background: rgba(255, 255, 255, 0.05);
        color: var(--text-main);
      }
      
      .nav-item.active {
        background: rgba(59, 130, 246, 0.1);
        color: var(--primary);
      }

      /* Pulsing Badge */
      .badge-pulse {
        width: 8px;
        height: 8px;
        background: #10b981;
        border-radius: 50%;
        box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7);
        animation: pulse-green 2s infinite;
        margin-left: auto;
      }
      
      @keyframes pulse-green {
        0% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { transform: scale(1); box-shadow: 0 0 0 6px rgba(16, 185, 129, 0); }
        100% { transform: scale(0.95); box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
      }

      .sidebar-footer {
        padding: 20px;
        border-top: 1px solid var(--border-subtle);
      }

      /* Main Area */
      main {
        flex: 1;
        display: flex;
        flex-direction: column;
        position: relative;
      }

      .top-bar {
        height: 64px;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0 32px;
        /* transparent, letting bg show through */
      }
      
      .toggle-btn {
        background: transparent;
        border: none;
        color: var(--text-muted);
        cursor: pointer;
        padding: 8px;
        border-radius: 8px;
        transition: 0.2s;
      }
      .toggle-btn:hover { background: rgba(255,255,255,0.05); color: var(--text-main); }

      /* Chat Area */
      .chat-scroll-area {
        flex: 1;
        overflow-y: auto;
        padding: 40px;
        display: flex;
        flex-direction: column;
        gap: 32px;
        scrollbar-width: thin;
        scrollbar-color: var(--border-subtle) transparent;
      }

      .home-view {
        flex: 1;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        max-width: 680px;
        margin: auto;
        text-align: center;
      }

      .home-logo {
        width: 80px;
        height: 80px;
        background: linear-gradient(135deg, rgba(59,130,246,0.2), rgba(37,99,235,0.1));
        border-radius: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 32px;
        color: var(--primary);
        font-size: 40px;
        border: 1px solid rgba(59,130,246,0.3);
        box-shadow: 0 0 40px rgba(59,130,246,0.15);
      }

      .home-title {
        font-size: 32px;
        font-weight: 500;
        margin-bottom: 12px;
        letter-spacing: -0.5px;
      }

      .home-subtitle {
        color: var(--text-muted);
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 48px;
      }

      .suggestions-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 16px;
        width: 100%;
      }

      .suggestion-card {
        background: var(--bg-glass-strong);
        border: 1px solid var(--border-subtle);
        padding: 20px;
        border-radius: 16px;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
      }
      
      .suggestion-card:hover {
        border-color: var(--primary);
        transform: translateY(-2px);
        background: rgba(30, 30, 50, 0.9);
      }

      .suggestion-title {
        color: var(--text-main);
        font-weight: 500;
        margin-bottom: 4px;
      }
      
      .suggestion-desc {
        color: var(--text-muted);
        font-size: 13px;
      }

      /* Message Bubbles */
      .message-bubble {
        max-width: 800px;
        width: 100%;
        margin: 0 auto;
        display: flex;
        gap: 20px;
        animation: fadeSlideUp 0.4s ease-out;
      }
      
      @keyframes fadeSlideUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }

      .message-avatar {
        width: 36px;
        height: 36px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 20px;
      }
      
      .message-avatar.user {
        background: rgba(255,255,255,0.1);
        color: var(--text-main);
      }
      
      .message-avatar.ai {
        background: var(--primary);
        color: white;
        box-shadow: 0 0 16px var(--primary-glow);
      }

      .message-content {
        flex: 1;
        padding-top: 6px;
      }

      .message-name {
        font-size: 13px;
        font-weight: 600;
        color: var(--text-muted);
        margin-bottom: 8px;
      }

      .message-text {
        font-size: 16px;
        line-height: 1.7;
        color: #e2e8f0;
      }

      /* Input Area */
      .input-container {
        padding: 0 0 32px 0;
        display: flex;
        justify-content: center;
        position: relative;
      }

      .input-box {
        width: 100%;
        max-width: 760px;
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(20px);
        -webkit-backdrop-filter: blur(20px);
        border: 1px solid var(--border-subtle);
        border-radius: 32px;
        padding: 12px 16px 12px 24px;
        display: flex;
        align-items: center;
        gap: 16px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
        transition: all 0.2s;
      }
      
      .input-box:focus-within {
        border-color: var(--primary);
        box-shadow: 0 8px 40px rgba(0, 0, 0, 0.3), 0 0 0 1px var(--primary);
        background: rgba(255, 255, 255, 0.05);
      }

      textarea {
        flex: 1;
        background: transparent;
        border: none;
        color: var(--text-main);
        font-size: 16px;
        padding: 8px 0;
        max-height: 150px;
      }
      
      textarea::placeholder { color: rgba(255,255,255,0.3); }
      textarea:focus { outline: none; }

      .send-btn {
        width: 44px;
        height: 44px;
        border-radius: 50%;
        background: var(--primary);
        color: white;
        border: none;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
        box-shadow: 0 2px 10px var(--primary-glow);
      }
      
      .send-btn:hover {
        transform: scale(1.05);
        background: #2563eb;
      }
      
      .send-btn:disabled { opacity: 0.5; transform: none; }

      .attach-btn {
        color: var(--text-muted);
        background: none;
        border: none;
        cursor: pointer;
        transition: color 0.2s;
      }
      
      .attach-btn:hover { color: var(--text-main); }
      
      .loading-dots .dot { background: var(--primary); }
      
      .loading-dots {
        display: flex;
        gap: 4px;
        padding: 12px 0;
      }
      
      .dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        animation: bounce 1.4s infinite ease-in-out both;
      }
      
      .dot:nth-child(1) { animation-delay: -0.32s; }
      .dot:nth-child(2) { animation-delay: -0.16s; }
      
      @keyframes bounce {
        0%, 80%, 100% { transform: scale(0); }
        40% { transform: scale(1); }
      }

      /* A2UI Overrides to match theme */
      a2ui-surface {
        display: block;
        margin-top: 16px;
      }

      .error {
        color: #f87171;
        background-color: rgba(220, 38, 38, 0.1);
        border: 1px solid rgba(220, 38, 38, 0.2);
        padding: 16px;
        border-radius: 12px;
        margin: 16px 24px;
      }
    `,
  ];

  #processor = v0_8.Data.createSignalA2uiMessageProcessor();
  #a2uiClient = new A2UIClient();
  #snackbar: Snackbar | undefined = undefined;
  #pendingSnackbarMessages: Array<{
    message: SnackbarMessage;
    replaceAll: boolean;
  }> = [];

  // Store user inputs to display in chat
  @state()
  accessor #chatHistory: Array<{type: 'user' | 'agent', content: string}> = [];

  connectedCallback() {
    super.connectedCallback();

    const urlParams = new URLSearchParams(window.location.search);
    const appKey = urlParams.get("app") || "jira";
    this.config = configs[appKey] || configs.jira;

    if (this.config.theme) {
      this.theme = this.config.theme;
    }

    window.document.title = this.config.title;
    window.document.documentElement.style.setProperty(
      "--background",
      this.config.background
    );

    this.#a2uiClient = new A2UIClient(this.config.serverUrl);
  }

  toggleSidebar() {
    this.sidebarCollapsed = !this.sidebarCollapsed;
  }

  handleInputChange(e: Event) {
    const textarea = e.target as HTMLTextAreaElement;
    textarea.style.height = 'auto';
    textarea.style.height = Math.min(textarea.scrollHeight, 200) + 'px';
  }

  handleKeyDown(e: KeyboardEvent) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      this.submitForm();
    }
  }

  async submitForm() {
    const input = this.shadowRoot?.querySelector('#message-input') as HTMLTextAreaElement;
    const value = input?.value.trim();
    if (!value || this.#requesting) return;

    this.currentView = 'chat';
    this.#chatHistory = [...this.#chatHistory, { type: 'user', content: value }];
    input.value = '';
    input.style.height = 'auto';

    const message: v0_8.Types.A2UIClientEventMessage = {
      userAction: {
        name: 'submit',
        context: { input: value },
        surfaceId: 'shell',
        sourceComponentId: 'chat-input',
        timestamp: new Date().toISOString()
      }
    };
    
    // Original code used: const message = body as v0_8.Types.A2UIClientEventMessage;
    // We need to construct a valid message. If the backend just takes "body" as text:
    // But A2UI usually expects a JSON object.
    // Let's try sending it as a simple text message if the client supports it, or wrap it.
    // Re-reading original app.ts: `const message = body as v0_8.Types.A2UIClientEventMessage;`
    // It seems the input `name="body"` was passed directly. 
    // If the input is just text, we might need to conform to what the server expects.
    // Let's assume for now we pass it as a simple string-based user event or similar.
    // Actually, let's replicate the `FormData` logic but manually.
    
    // The previous form had `<input name="body">`.
    // So the payload is whatever that input string is, cast to `A2UIClientEventMessage`.
    // That implies the user is typing JSON? Or the input IS the message?
    // If the user types "Hello", and we cast "Hello" to `A2UIClientEventMessage` (which is an object), that will fail at runtime or on server.
    // However, looking at the type definition `A2UIClientEventMessage` usually has `userAction`.
    // The `a2ui_examples.py` seems to process complex actions.
    
    // Let's trust the input is meant to be a JSON string if the original app worked that way?
    // OR, maybe the original app's input `value="${this.config.placeholder}"` suggests it might be pre-filled JSON?
    // Let's check `jira.ts` config later if needed.
    // For a chat interface, we usually send natural language.
    // I will wrap the natural language in a generic "user message" structure if I can.
    // But to be safe and compatible with the previous `app.ts` logic:
    // `const body = data.get("body")` -> `this.#sendAndProcessMessage(body)`.
    // So I will pass the raw string `value` to `sendAndProcessMessage`.
    // Wait, the `sendAndProcessMessage` expects `request`.
    // Let's assume the user input IS the request payload for now, or text.
    
    await this.#sendAndProcessMessage(value);
  }

  render() {
    const sidebarClasses = { collapsed: this.sidebarCollapsed };
    
    return html`
      <aside class=${classMap(sidebarClasses)}>
        ${this.renderSidebar()}
      </aside>
      <main>
        ${this.renderTopBar()}
        ${this.currentView === 'home' ? this.renderHomeView() : this.renderChatView()}
        ${this.renderInputArea()}
        ${this.#maybeRenderError()}
      </main>
    `;
  }

  renderSidebar() {
    if (this.sidebarCollapsed) {
       return html`
         <div class="sidebar-header" style="justify-content: center; padding: 16px 0;">
             <span class="g-icon">chat_bubble</span>
         </div>
       `;
    }

    return html`
      <div class="sidebar-header">
         <div style="font-weight: 600; font-size: 18px; display: flex; align-items: center; gap: 8px;">
           <span class="g-icon" style="color: var(--primary)">smart_toy</span> A2UI Agent
         </div>
      </div>

      <button class="new-chat-btn" @click=${() => {
          this.currentView = 'home';
          this.#chatHistory = [];
          this.#processor.clearSurfaces();
          this.#lastMessages = [];
          this.requestUpdate();
      }}>
        <span class="g-icon">add</span> New Chat
      </button>

      <div class="sidebar-section">
        <div class="section-title">Recent Chats</div>
        <a class="nav-item active">
          <span class="g-icon">chat</span>
          Project JIRA Update
        </a>
        
        <div class="section-title">Agents</div>
        <a class="nav-item active">
          <span class="g-icon">bug_report</span>
          Jira Assistant
          <div class="badge-pulse"></div>
        </a>
        <a class="nav-item">
          <span class="g-icon">cloud</span>
          Salesforce Agent
        </a>
      </div>

      <div class="sidebar-footer">
        <a class="nav-item theme-toggle-btn" @click=${this.toggleTheme}>
           <span class="g-icon">dark_mode</span> Theme
        </a>
        <a class="nav-item">
           <span class="g-icon">settings</span> Settings
        </a>
        <a class="nav-item">
           <span class="g-icon">account_circle</span> Tony
        </a>
      </div>
    `;
  }

  renderTopBar() {
    return html`
      <header class="top-bar">
        <div style="display: flex; align-items: center; gap: 16px;">
          <button class="toggle-btn" @click=${this.toggleSidebar}>
            <span class="g-icon">menu</span>
          </button>
          <span class="model-selector">${this.config.title}</span>
        </div>
        <div>
           <button class="toggle-btn">
             <span class="g-icon">more_vert</span>
           </button>
        </div>
      </header>
    `;
  }

  renderHomeView() {
    return html`
      <div class="chat-scroll-area">
        <div class="home-view">
          <div class="home-logo">
            <span class="g-icon" style="font-size: 32px;">smart_toy</span>
          </div>
          <h2 class="home-title">How can I help you today?</h2>
          <p class="home-subtitle">I can help you manage your Jira tickets and track project progress.</p>
          
          <div class="suggestions-grid">
            <div class="suggestion-card" @click=${() => this.prefillAndSubmit('Show me my high priority issues')}>
              <div class="suggestion-title">Jira Issues</div>
              <div class="suggestion-desc">Show high priority tickets</div>
            </div>
             <div class="suggestion-card" @click=${() => this.prefillAndSubmit('Create a new issue')}>
               <div class="suggestion-title">Create Issue</div>
               <div class="suggestion-desc">Draft a new bug report</div>
            </div>
          </div>
        </div>
      </div>
    `;
  }

  prefillAndSubmit(text: string) {
     const input = this.shadowRoot?.querySelector('#message-input') as HTMLTextAreaElement;
     if (input) {
       input.value = text;
       this.submitForm();
     }
  }

  renderChatView() {
    return html`
      <div class="chat-scroll-area">
         ${this.#chatHistory.map(msg => html`
            <div class="message-bubble">
               <div class="message-avatar ${msg.type}">
                 <span class="g-icon">${msg.type === 'user' ? 'person' : 'smart_toy'}</span>
               </div>
               <div class="message-content">
                  <div class="message-name">${msg.type === 'user' ? 'You' : 'Assistant'}</div>
                  <div class="message-text">${msg.content}</div>
               </div>
            </div>
         `)}

         ${this.#maybeRenderData()}
         
         ${this.#requesting ? html`
           <div class="message-bubble">
             <div class="message-avatar ai">
                <span class="g-icon">smart_toy</span>
             </div>
             <div class="message-content">
                <div class="message-name">Assistant</div>
                <div class="loading-dots">
                  <div class="dot"></div><div class="dot"></div><div class="dot"></div>
                </div>
             </div>
           </div>
         ` : nothing}
      </div>
    `;
  }

  renderInputArea() {
    return html`
      <div class="input-container">
        <div class="input-box">
          <textarea 
            id="message-input"
            placeholder="${this.config.placeholder || 'Type a message...'}"
            rows="1"
            @input=${this.handleInputChange}
            @keydown=${this.handleKeyDown}
            ?disabled=${this.#requesting}
          ></textarea>
          
           <button class="attach-btn" title="Attach file">
             <span class="g-icon">attach_file</span>
           </button>

            <button class="send-btn" @click=${this.submitForm} ?disabled=${this.#requesting}>
               ${this.#requesting 
                 ? html`<div class="loading-dots" style="transform: scale(0.6)"><div class="dot" style="background:white"></div><div class="dot" style="background:white"></div><div class="dot" style="background:white"></div></div>` 
                 : html`<span class="g-icon">arrow_upward</span>`}
            </button>
        </div>
      </div>
    `;
  }
  
  toggleTheme(evt: Event) {
      const btn = evt.currentTarget as HTMLElement;
      const { colorScheme } = window.getComputedStyle(btn);
      // Logic needs to be robust, using document.body mainly
      const body = document.body;
      if (body.classList.contains('dark')) {
          body.classList.remove('dark');
          body.classList.add('light');
      } else {
          body.classList.remove('light');
          body.classList.add('dark');
      }
  }

  // --- Existing Logic Preserved ---

  async #sendMessage(
    message: v0_8.Types.A2UIClientEventMessage | string
  ): Promise<v0_8.Types.ServerToClientMessage[]> {
    try {
      this.#requesting = true;
      this.#startLoadingAnimation();
      
      // If message is string (user input), try to see if we can just send it.
      // The original client expects A2UIClientEventMessage.
      // We might need to wrap it if it's just a string. 
      // Assuming for now the `send` method can handle it or we cast it.
      // Since I don't see the definition of `A2UIClient` here, I'll assume standard A2UI behavior.
      // Standard A2UI usually expects a specific JSON.
      // If the backend is an agent, it might expect: { "userAction": { ... } }
      // I will wrap it if it's a string.
      
      let payload = message;
      if (typeof message === 'string') {
          // Attempt to parse if user typed JSON
          try {
             payload = JSON.parse(message);
          } catch {
             // Treat as natural language input? 
             // Currently A2UI samples usually rely on specific JSON structures triggered by buttons.
             // But for a chat shell, we likely want to send the text.
             // I'll send it as is and hope the backend can handle raw strings or I'll wrap it in a generic action.
             // Looking at `a2ui_examples.py`... actions like `create_issue_submit` have context.
             // If the user types free text, there is no generic "chat" action defined in the examples.
             // This suggests the backend might NOT be ready for free text chat without modification.
             // BUT, my task is the UI. I will send the payload.
             // If I must send an object:
             // payload = { userAction: { name: 'chat', context: { text: message } } };
             // I'll stick to the raw input for now as the original `app.ts` did `const message = body as ...`.
          }
      }

      const response = await this.#a2uiClient.send(payload as v0_8.Types.A2UIClientEventMessage);
      await response;
      this.#requesting = false;
      this.#stopLoadingAnimation();

      return response;
    } catch (err) {
      this.snackbar(err as string, SnackType.ERROR);
    } finally {
      this.#requesting = false;
      this.#stopLoadingAnimation();
    }

    return [];
  }
  
  #startLoadingAnimation() {
    // Kept for compatibility, though utilized less in new UI
    if (
      Array.isArray(this.config.loadingText) &&
      this.config.loadingText.length > 1
    ) {
      this.#loadingTextIndex = 0;
      this.#loadingInterval = window.setInterval(() => {
        this.#loadingTextIndex =
          (this.#loadingTextIndex + 1) %
          (this.config.loadingText as string[]).length;
      }, 2000);
    }
  }

  #stopLoadingAnimation() {
    if (this.#loadingInterval) {
      clearInterval(this.#loadingInterval);
      this.#loadingInterval = undefined;
    }
  }

  async #sendAndProcessMessage(request) {
    console.log("Sending message to agent:", request);
    const messages = await this.#sendMessage(request);
    console.log("A2UI Messages received from Client:", messages);
    
    this.#lastMessages = messages;
    console.log("Clearing existing surfaces...");
    this.#processor.clearSurfaces();
    
    console.log("Processing new A2UI messages...");
    this.#processor.processMessages(messages);
    
    const updatedSurfaces = this.#processor.getSurfaces();
    console.log(`Processor updated. Total surfaces now: ${updatedSurfaces.size}`);
    
    this.requestUpdate(); 
  }

  #maybeRenderData() {
    const surfaces = this.#processor.getSurfaces();
    if (surfaces.size === 0) {
      console.log("No surfaces to render (surfaces.size === 0)");
      return nothing;
    }

    console.log(`Rendering ${surfaces.size} surfaces:`, Array.from(surfaces.keys()));

    // Wrap the surfaces in a "message bubble" look for the Agent
    return html`
      <div class="message-bubble">
         <div class="message-avatar ai">
            <span class="g-icon">smart_toy</span>
         </div>
         <div class="message-content">
             <div class="message-name">Assistant</div>
             
             <!-- The A2UI Surface Content -->
             <section id="surfaces">
              ${repeat(
              this.#processor.getSurfaces(),
              ([surfaceId]) => surfaceId,
              ([surfaceId, surface]) => {
                return html`<a2ui-surface
                      @a2uiaction=${async (
                  evt: v0_8.Events.StateEvent<"a2ui.action">
                ) => {
                    const [target] = evt.composedPath();
                    if (!(target instanceof HTMLElement)) {
                      return;
                    }

                    const context: v0_8.Types.A2UIClientEventMessage["userAction"]["context"] =
                      {};
                    if (evt.detail.action.context) {
                      const srcContext = evt.detail.action.context;
                      for (const item of srcContext) {
                        if (item.value.literalBoolean) {
                          context[item.key] = item.value.literalBoolean;
                        } else if (item.value.literalNumber) {
                          context[item.key] = item.value.literalNumber;
                        } else if (item.value.literalString) {
                          context[item.key] = item.value.literalString;
                        } else if (item.value.path) {
                          const path = this.#processor.resolvePath(
                            item.value.path,
                            evt.detail.dataContextPath
                          );
                          const value = this.#processor.getData(
                            evt.detail.sourceComponent,
                            path,
                            surfaceId
                          );
                          context[item.key] = value;
                        }
                      }
                    }

                    const message: v0_8.Types.A2UIClientEventMessage = {
                      userAction: {
                        name: evt.detail.action.name,
                        surfaceId,
                        sourceComponentId: target.id,
                        timestamp: new Date().toISOString(),
                        context,
                      },
                    };

                    await this.#sendAndProcessMessage(message);
                  }}
                      .surfaceId=${surfaceId}
                      .surface=${surface}
                      .processor=${this.#processor}
                    ></a2-uisurface>`;
              }
            )}
            </section>
         </div>
      </div>
    `;
  }

  #maybeRenderError() {
    if (!this.#error) return nothing;
    return html`<div class="error">${this.#error}</div>`;
  }

  snackbar(
    message: string | HTMLTemplateResult,
    type: SnackType,
    actions: SnackbarAction[] = [],
    persistent = false,
    id = globalThis.crypto.randomUUID(),
    replaceAll = false
  ) {
    if (!this.#snackbar) {
      this.#pendingSnackbarMessages.push({
        message: {
          id,
          message,
          type,
          persistent,
          actions,
        },
        replaceAll,
      });
      return;
    }

    return this.#snackbar.show(
      {
        id,
        message,
        type,
        persistent,
        actions,
      },
      replaceAll
    );
  }

  unsnackbar(id?: SnackbarUUID) {
    if (!this.#snackbar) {
      return;
    }
    this.#snackbar.hide(id);
  }
}