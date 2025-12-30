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
from typing import Any, List, Optional

logger = logging.getLogger(__name__)

from google.adk.tools.application_integration_tool.application_integration_toolset import ApplicationIntegrationToolset

connector_tool = ApplicationIntegrationToolset(
    project="truiz-agent-builder", # TODO: replace with GCP project of the connection
    location="us-central1", #TODO: replace with location of the connection
    connection="salesforce-conn", #TODO: replace with connection name
    entity_operations={"User": ["LIST","CREATE", "GET", "UPDATE"], 
                       "Lead": ["LIST","CREATE", "GET", "UPDATE"],
                        "Campaign":["LIST","CREATE", "GET", "UPDATE"],
                        "Opportunity":["LIST","CREATE", "GET", "UPDATE"],
                        "Case":["LIST","CREATE", "GET", "UPDATE"],
                        "Account":["LIST","CREATE", "GET", "UPDATE"],
                        
                        },#empty list for actions means all operations on the entity are supported.
    # actions=["action1"], #TODO: replace with actions
    # service_account_json='{...}', # optional. Stringified json for service account key
    tool_name_prefix="Salesforce Tool",
    tool_instructions="A tool for interacting with Salesforce. You can fetch user and account data, search and create Opportunities, leads , and view and create campaigns"
)



# # Mock data for Salesforce entities
# MOCK_DATA = {
#     "User": [
#         {"id": "U001", "name": "Alice Johnson", "email": "alice@example.com", "role": "Sales Manager"},
#         {"id": "U002", "name": "Bob Smith", "email": "bob@example.com", "role": "Sales Rep"},
#     ],
#     "Lead": [
#         {"id": "L001", "name": "Acme Corp Lead", "company": "Acme Corp", "status": "New", "email": "contact@acme.com"},
#         {"id": "L002", "name": "Globex Lead", "company": "Globex", "status": "Working", "email": "contact@globex.com"},
#     ],
#     "Campaign": [
#         {"id": "C001", "name": "Q1 Outreach", "status": "Active", "type": "Email"},
#         {"id": "C002", "name": "Webinar Series", "status": "Planned", "type": "Webinar"},
#     ],
#     "Account": [
#         {"id": "A001", "name": "Acme Corp", "industry": "Technology", "phone": "555-0100"},
#         {"id": "A002", "name": "Globex Corporation", "industry": "Manufacturing", "phone": "555-0101"},
#     ],
#     "Opportunity": [
#         {"id": "O001", "name": "Acme 500 Licenses", "stage": "Negotiation", "amount": 50000, "accountId": "A001"},
#         {"id": "O002", "name": "Globex Service Contract", "stage": "Prospecting", "amount": 12000, "accountId": "A002"},
#     ],
#     "Case": [
#         {"id": "CS001", "subject": "Login Issue", "status": "New", "priority": "High", "accountId": "A001"},
#         {"id": "CS002", "subject": "Billing Question", "status": "Closed", "priority": "Medium", "accountId": "A002"},
#     ]
# }

# def get_salesforce_data(entity: str, query: str = None) -> List[dict[str, Any]]:
#     """
#     Fetches Salesforce data for a specific entity type, optionally filtered by a query.

#     Args:
#         entity: The type of entity to fetch (User, Lead, Campaign, Account, Opportunity, Case).
#         query: A text query to filter the results.

#     Returns:
#         A list of matching records.
#     """
#     logger.info(f"Tool called: get_salesforce_data(entity={entity}, query={query})")
    
#     data = MOCK_DATA.get(entity, [])
    
#     if not query:
#         return data

#     q = query.lower()
    
#     def match(record):
#         # Match against any string value in the record
#         for val in record.values():
#             if isinstance(val, str) and q in val.lower():
#                 return True
#             if isinstance(val, (int, float)) and q in str(val):
#                 return True
#         return False

#     results = [record for record in data if match(record)]
#     return results
