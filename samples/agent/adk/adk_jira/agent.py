# Copyright 2025 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
from collections.abc import AsyncIterable
from typing import Any

import jsonschema
from a2ui_examples import JIRA_UI_EXAMPLES
from a2ui_schema import A2UI_SCHEMA
from google.adk.agents.llm_agent import LlmAgent
from google.adk.artifacts import InMemoryArtifactService
from google.adk.memory.in_memory_memory_service import InMemoryMemoryService
from google.adk.models.lite_llm import LiteLlm
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types
from prompt_builder import (
    get_text_prompt,
    get_ui_prompt,
)
# from tools import get_jira_issues
from tools import connector_tool 

logger = logging.getLogger(__name__)


class JiraAgent:
    """An agent that manages Jira issues."""

    SUPPORTED_CONTENT_TYPES = ["text", "text/plain"]

    def __init__(self, base_url: str, use_ui: bool = False):
        self.base_url = base_url
        self.use_ui = use_ui
        self._agent = self._build_agent(use_ui)
        self._user_id = "remote_agent"
        self._runner = Runner(
            app_name=self._agent.name,
            agent=self._agent,
            artifact_service=InMemoryArtifactService(),
            session_service=InMemorySessionService(),
            memory_service=InMemoryMemoryService(),
        )

        try:
            single_message_schema = json.loads(A2UI_SCHEMA)
            self.a2ui_schema_object = {"type": "array", "items": single_message_schema}
            logger.info("A2UI_SCHEMA successfully loaded and wrapped in an array validator.")
        except json.JSONDecodeError as e:
            logger.error(f"CRITICAL: Failed to parse A2UI_SCHEMA: {e}")
            self.a2ui_schema_object = None

    def get_processing_message(self) -> str:
        return "Processing Jira request..."

    def _build_agent(self, use_ui: bool) -> LlmAgent:
        """Builds the LLM agent for the jira agent."""
        LITELLM_MODEL = os.getenv("LITELLM_MODEL", "gemini/gemini-2.5-flash")

        if use_ui:
            instruction = get_ui_prompt(self.base_url, JIRA_UI_EXAMPLES)
        else:
            instruction = get_text_prompt()

        return LlmAgent(
            model= "gemini-3-flash-preview",#LiteLlm(model=LITELLM_MODEL),
            name="jira_agent",
            description="An agent that manages Jira issues.",
            instruction=instruction,
            # tools=[get_jira_issues],
            tools=[connector_tool]
        )

    async def stream(self, query, session_id) -> AsyncIterable[dict[str, Any]]:
        session_state = {"base_url": self.base_url}

        session = await self._runner.session_service.get_session(
            app_name=self._agent.name,
            user_id=self._user_id,
            session_id=session_id,
        )
        if session is None:
            session = await self._runner.session_service.create_session(
                app_name=self._agent.name,
                user_id=self._user_id,
                state=session_state,
                session_id=session_id,
            )
        elif "base_url" not in session.state:
            session.state["base_url"] = self.base_url

        max_retries = 1
        attempt = 0
        current_query_text = query

        if self.use_ui and self.a2ui_schema_object is None:
            yield {
                "is_task_complete": True,
                "content": "I'm sorry, I'm facing an internal configuration error with my UI components.",
            }
            return

        while attempt <= max_retries:
            attempt += 1
            current_message = types.Content(
                role="user", parts=[types.Part.from_text(text=current_query_text)]
            )
            final_response_content = None

            async for event in self._runner.run_async(
                user_id=self._user_id,
                session_id=session.id,
                new_message=current_message,
            ):
                if event.is_final_response():
                    if event.content and event.content.parts and event.content.parts[0].text:
                        final_response_content = "\n".join([p.text for p in event.content.parts if p.text])
                    break
                else:
                    yield {
                        "is_task_complete": False,
                        "updates": self.get_processing_message(),
                    }

            if final_response_content is None:
                if attempt <= max_retries:
                    current_query_text = f"I received no response. Please retry the original request: '{query}'"
                    continue
                else:
                    final_response_content = "I'm sorry, I encountered an error and couldn't process your request."

            is_valid = False
            error_message = ""

            if self.use_ui:
                try:
                    if "---a2ui_JSON---" not in final_response_content:
                        raise ValueError("Delimiter '---a2ui_JSON---' not found.")

                    text_part, json_string = final_response_content.split("---a2ui_JSON---", 1)
                    json_string_cleaned = json_string.strip().lstrip("```json").rstrip("```").strip()
                    
                    if not json_string.strip() or json_string_cleaned == "[]":
                        is_valid = True
                    else:
                        parsed_json_data = json.loads(json_string_cleaned)
                        jsonschema.validate(instance=parsed_json_data, schema=self.a2ui_schema_object)
                        is_valid = True

                except (ValueError, json.JSONDecodeError, jsonschema.exceptions.ValidationError) as e:
                    error_message = f"Validation failed: {e}."

            else:
                is_valid = True

            if is_valid:
                yield {
                    "is_task_complete": True,
                    "content": final_response_content,
                }
                return

            if attempt <= max_retries:
                current_query_text = (
                    f"Your previous response was invalid. {error_message} "
                    "You MUST generate a valid response that strictly follows the A2UI JSON SCHEMA. "
                    "The response MUST be a JSON list of A2UI messages. "
                    "Ensure the response is split by '---a2ui_JSON---' and the JSON part is well-formed. "
                    f"Please retry the original request: '{query}'"
                )

        yield {
            "is_task_complete": True,
            "content": "I'm sorry, I'm having trouble generating the interface for that request right now.",
        }
