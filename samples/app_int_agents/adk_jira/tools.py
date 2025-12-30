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

# Mock data for demonstration
MOCK_ISSUES = [
    {
        "key": "PROJ-123",
        "summary": "Fix login bug",
        "status": "In Progress",
        "priority": "High",
        "assignee": "Tony",
        "project": "PROJ"
    },
    {
        "key": "PROJ-456",
        "summary": "Add search feature",
        "status": "To Do",
        "priority": "Medium",
        "assignee": "None",
        "project": "PROJ"
    },
    {
        "key": "OTHER-789",
        "summary": "Update readme",
        "status": "Done",
        "priority": "Low",
        "assignee": "Alice",
        "project": "OTHER"
    }
]

def get_jira_issues(query: str = None, project: str = None) -> list[dict[str, Any]]:
    """
    Finds Jira issues based on a query or project.

    Args:
        query: A text query to search in summaries.
        project: The project key to filter by.

    Returns:
        A list of matching Jira issues.
    """
    logger.info(f"Tool called: get_jira_issues(query={query}, project={project})")
    
    results = MOCK_ISSUES
    if project:
        results = [i for i in results if i["project"].upper() == project.upper()]
    if query:
        results = [i for i in results if query.lower() in i["summary"].lower()]
        
    return results
