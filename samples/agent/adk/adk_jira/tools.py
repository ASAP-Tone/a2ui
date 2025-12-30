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

import logging
from typing import Any

logger = logging.getLogger(__name__)
from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

connector_tool = ApplicationIntegrationToolset(
    project="truiz-agent-builder", # TODO: replace with GCP project of the connection
    location="us-central1", #TODO: replace with location of the connection
    connection="jira-conn", #TODO: replace with connection name
    entity_operations={"Issues": ["LIST","CREATE", "GET", "UPDATE"], 
                       "Comments": ["LIST","CREATE", "GET", "UPDATE"],
                        "Users":["LIST","CREATE", "GET", "UPDATE"] },#empty list for actions means all operations on the entity are supported.
    # actions=["action1"], #TODO: replace with actions
    # service_account_json='{...}', # optional. Stringified json for service account key
    tool_name_prefix="Jira Tool",
    tool_instructions="A tool for interacting with Jira. You can fetch user data, search and create issues, and view and create comments"
)


# # Mock data for demonstration
# MOCK_ISSUES = [
#     {
#         "key": "PROJ-123",
#         "summary": "Fix login bug",
#         "status": "In Progress",
#         "priority": "High",
#         "assignee": "Tony",
#         "project": "PROJ"
#     },
#     {
#         "key": "PROJ-456",
#         "summary": "Add search feature",
#         "status": "To Do",
#         "priority": "Medium",
#         "assignee": "None",
#         "project": "PROJ"
#     },
#     {
#         "key": "OTHER-789",
#         "summary": "Update readme",
#         "status": "Done",
#         "priority": "Low",
#         "assignee": "Alice",
#         "project": "OTHER"
#     }
# ]

# def get_jira_issues(query: str = None, project: str = None) -> list[dict[str, Any]]:
#     """
#     Finds Jira issues based on a query or project.

#     Args:
#         query: A text query to search in summaries.
#         project: The project key to filter by.

#     Returns:
#         A list of matching Jira issues.
#     """
#     logger.info(f"Tool called: get_jira_issues(query={query}, project={project})")
    
#     results = MOCK_ISSUES
#     logger.info( results )
#     for i in results:
#         logger.info( i )
#     # if project:
#     #     results = [i for i in results if i["project"].upper() == project.upper()]
#     if query:
#         results = [i for i in results if query.lower() in i["key"].lower()]
        
#     return results
