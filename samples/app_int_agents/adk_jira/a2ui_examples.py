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

JIRA_UI_EXAMPLES = r"""
--- ISSUE_DETAIL_EXAMPLE ---
[
  {
    "surfaceId": "jira_issue_detail",
    "beginRendering": {
      "root": "issue_root",
      "surfaceId": "jira_issue_detail",
      "styles": {
        "primaryColor": "#0052CC"
      }
    }
  },
  {
    "surfaceId": "jira_issue_detail",
    "dataModelUpdate": {
      "surfaceId": "jira_issue_detail",
      "contents": [
        { "key": "key", "valueString": "PROJ-123" },
        { "key": "summary", "valueString": "Update documentation for A2UI" },
        { "key": "status", "valueString": "In Progress" },
        { "key": "priority", "valueString": "High" },
        { "key": "assignee", "valueString": "Tony" }
      ]
    }
  },
  {
    "surfaceId": "jira_issue_detail",
    "surfaceUpdate": {
      "surfaceId": "jira_issue_detail",
      "components": [
        {
          "id": "issue_root",
          "component": {
            "Card": {
              "child": "issue_col"
            }
          }
        },
        {
          "id": "issue_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["issue_header", "issue_details", "issue_actions"]
              }
            }
          }
        },
        {
          "id": "issue_header",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["issue_key", "issue_status"]
              },
              "distribution": "spaceBetween"
            }
          }
        },
        {
          "id": "issue_key",
          "component": {
            "Text": {
              "text": { "path": "/key" },
              "usageHint": "h3"
            }
          }
        },
        {
          "id": "issue_status",
          "component": {
            "Text": {
              "text": { "path": "/status" },
              "usageHint": "caption"
            }
          }
        },
        {
          "id": "issue_details",
          "component": {
            "Text": {
              "text": { "path": "/summary" },
              "usageHint": "body"
            }
          }
        },
        {
          "id": "issue_actions",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["assign_btn", "close_btn"]
              },
              "distribution": "end"
            }
          }
        },
        {
          "id": "assign_btn",
          "component": {
            "Button": {
              "child": "assign_text",
              "primary": true,
              "action": {
                "name": "assign_issue",
                "context": [
                  { "key": "issue_key", "value": { "path": "/key" } }
                ]
              }
            }
          }
        },
        {
          "id": "assign_text",
          "component": {
            "Text": { "text": { "literalString": "Assign to me" } }
          }
        },
        {
          "id": "close_btn",
          "component": {
            "Button": {
              "child": "close_text",
              "action": {
                "name": "close_issue",
                "context": [
                  { "key": "issue_key", "value": { "path": "/key" } }
                ]
              }
            }
          }
        },
        {
          "id": "close_text",
          "component": {
            "Text": { "text": { "literalString": "Close" } }
          }
        }
      ]
    }
  }
]

--- ISSUE_LIST_EXAMPLE ---
[
  {
    "surfaceId": "jira_issue_list",
    "beginRendering": {
      "root": "list_root",
      "surfaceId": "jira_issue_list",
      "styles": {
        "primaryColor": "#0052CC"
      }
    }
  },
  {
    "surfaceId": "jira_issue_list",
    "dataModelUpdate": {
      "surfaceId": "jira_issue_list",
      "contents": [
        {
          "key": "issues",
          "valueMap": [
            {
              "key": "issue1",
              "valueMap": [
                { "key": "key", "valueString": "PROJ-1" },
                { "key": "summary", "valueString": "Fix bug in renderer" }
              ]
            },
            {
              "key": "issue2",
              "valueMap": [
                { "key": "key", "valueString": "PROJ-2" },
                { "key": "summary", "valueString": "Add new component" }
              ]
            }
          ]
        }
      ]
    }
  },
  {
    "surfaceId": "jira_issue_list",
    "surfaceUpdate": {
      "surfaceId": "jira_issue_list",
      "components": [
        {
          "id": "list_root",
          "component": {
            "Column": {
              "children": {
                "template": {
                  "componentId": "issue_item",
                  "dataBinding": "/issues"
                }
              }
            }
          }
        },
        {
          "id": "issue_item",
          "component": {
            "Card": {
              "child": "item_row"
            }
          }
        },
        {
          "id": "item_row",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["item_key", "item_summary"]
              }
            }
          }
        },
        {
          "id": "item_key",
          "component": {
            "Text": {
              "text": { "path": "key" },
              "usageHint": "h5"
            }
          }
        },
        {
          "id": "item_summary",
          "component": {
            "Text": {
              "text": { "path": "summary" },
              "usageHint": "body"
            }
          }
        }
      ]
    }
  }
]
"""
