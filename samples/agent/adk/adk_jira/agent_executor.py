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

from a2a.server.agent_execution import AgentExecutor, RequestContext
from a2a.server.events import EventQueue
from a2a.server.tasks import TaskUpdater
from a2a.types import (
    DataPart,
    Part,
    Task,
    TaskState,
    TextPart,
    UnsupportedOperationError,
)
from a2a.utils import (
    new_agent_parts_message,
    new_agent_text_message,
    new_task,
)
from a2a.utils.errors import ServerError
from agent import JiraAgent
from a2ui.a2ui_extension import create_a2ui_part, try_activate_a2ui_extension

logger = logging.getLogger(__name__)


class JiraAgentExecutor(AgentExecutor):
    """Jira AgentExecutor Example."""

    def __init__(self, base_url: str):
        self.ui_agent = JiraAgent(base_url=base_url, use_ui=True)
        self.text_agent = JiraAgent(base_url=base_url, use_ui=False)

    async def execute(
        self,
        context: RequestContext,
        event_queue: EventQueue,
    ) -> None:
        query = ""
        ui_event_part = None
        action = None

        use_ui = try_activate_a2ui_extension(context)

        if use_ui:
            agent = self.ui_agent
        else:
            agent = self.text_agent

        if context.message and context.message.parts:
            for part in context.message.parts:
                if isinstance(part.root, DataPart):
                    if "userAction" in part.root.data:
                        ui_event_part = part.root.data["userAction"]

        if ui_event_part:
            action = ui_event_part.get("name")
            ctx = ui_event_part.get("context", {})

            if action == "assign_issue":
                issue_key = ctx.get("issue_key", "Unknown")
                query = f"ACTION: Assign issue {issue_key} to me"
            elif action == "close_issue":
                issue_key = ctx.get("issue_key", "Unknown")
                query = f"ACTION: Close issue {issue_key}"
            else:
                query = f"User submitted an event: {action} with data: {ctx}"
        else:
            query = context.get_user_input()

        task = context.current_task

        if not task:
            task = new_task(context.message)
            await event_queue.enqueue_event(task)
        updater = TaskUpdater(event_queue, task.id, task.context_id)

        async for item in agent.stream(query, task.context_id):
            is_task_complete = item["is_task_complete"]
            if not is_task_complete:
                await updater.update_status(
                    TaskState.working,
                    new_agent_text_message(item["updates"], task.context_id, task.id),
                )
                continue

            final_state = TaskState.input_required
            if action in ["assign_issue", "close_issue"]:
                 final_state = TaskState.completed

            content = item["content"]
            final_parts = []
            if "---a2ui_JSON---" in content:
                text_content, json_string = content.split("---a2ui_JSON---", 1)

                if text_content.strip():
                    final_parts.append(Part(root=TextPart(text=text_content.strip())))

                if json_string.strip():
                    try:
                        json_string_cleaned = (
                            json_string.strip().lstrip("```json").rstrip("```").strip()
                        )
                        
                        if not json_string_cleaned or json_string_cleaned == "[]":
                            pass
                        else:
                            json_data = json.loads(json_string_cleaned)
                            if isinstance(json_data, list):
                                for message in json_data:
                                    final_parts.append(create_a2ui_part(message))
                            else:
                                final_parts.append(create_a2ui_part(json_data))
 
                    except json.JSONDecodeError as e:
                        logger.error(f"Failed to parse UI JSON: {e}")
                        final_parts.append(Part(root=TextPart(text=json_string)))
            else:
                final_parts.append(Part(root=TextPart(text=content.strip())))

            if not final_parts or all(isinstance(p.root, TextPart) and not p.root.text for p in final_parts):
                 final_parts = [Part(root=TextPart(text="OK."))]

            await updater.update_status(
                final_state,
                new_agent_parts_message(final_parts, task.context_id, task.id),
                final=(final_state == TaskState.completed),
            )
            break

    async def cancel(
        self, request: RequestContext, event_queue: EventQueue
    ) -> Task | None:
        raise ServerError(error=UnsupportedOperationError())
