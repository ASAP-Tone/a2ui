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
--- ISSUE_DETAIL_WITH_COMMENTS_EXAMPLE ---
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
        { "key": "description", "valueString": "The documentation needs to be updated to reflect the new API changes." },
        { "key": "status", "valueString": "In Progress" },
        { "key": "priority", "valueString": "High" },
        { "key": "assignee", "valueString": "Tony" },
        {
          "key": "comments",
          "valueMap": [
            {
              "key": "comment1",
              "valueMap": [
                { "key": "author", "valueString": "Alice" },
                { "key": "body", "valueString": "I can help with this." }
              ]
            },
            {
              "key": "comment2",
              "valueMap": [
                { "key": "author", "valueString": "Bob" },
                { "key": "body", "valueString": "Great, let me know if you need review." }
              ]
            }
          ]
        },
        { "key": "new_comment", "valueString": "" }
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
              "child": "issue_content_col"
            }
          }
        },
        {
          "id": "issue_content_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["issue_header", "issue_summary", "issue_description", "issue_meta", "actions_row", "comments_section"]
              },
              "distribution": "start",
              "alignment": "stretch"
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
          "id": "issue_summary",
          "component": {
            "Text": {
              "text": { "path": "/summary" },
              "usageHint": "h5"
            }
          }
        },
        {
          "id": "issue_description",
          "component": {
            "Text": {
              "text": { "path": "/description" },
              "usageHint": "body"
            }
          }
        },
        {
          "id": "issue_meta",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["priority_label", "priority_val", "assignee_label", "assignee_val"]
              },
              "distribution": "start"
            }
          }
        },
        {
          "id": "priority_label",
          "component": { "Text": { "text": { "literalString": "Priority: " }, "usageHint": "caption" } }
        },
        {
          "id": "priority_val",
          "component": { "Text": { "text": { "path": "/priority" }, "usageHint": "body" } }
        },
        {
          "id": "assignee_label",
          "component": { "Text": { "text": { "literalString": " | Assignee: " }, "usageHint": "caption" } }
        },
        {
          "id": "assignee_val",
          "component": { "Text": { "text": { "path": "/assignee" }, "usageHint": "body" } }
        },
        {
          "id": "actions_row",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["edit_btn", "assign_me_btn"]
              },
              "distribution": "end"
            }
          }
        },
        {
          "id": "edit_btn",
          "component": {
            "Button": {
              "child": "edit_text",
              "action": {
                "name": "edit_issue",
                "context": [{ "key": "key", "value": { "path": "/key" } }]
              }
            }
          }
        },
        {
          "id": "edit_text",
          "component": { "Text": { "text": { "literalString": "Edit" } } }
        },
        {
          "id": "assign_me_btn",
          "component": {
            "Button": {
              "child": "assign_me_text",
              "primary": true,
              "action": {
                "name": "assign_issue_to_me",
                "context": [{ "key": "key", "value": { "path": "/key" } }]
              }
            }
          }
        },
        {
          "id": "assign_me_text",
          "component": { "Text": { "text": { "literalString": "Assign to Me" } } }
        },
        {
          "id": "comments_section",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["comments_header", "comments_list", "add_comment_row"]
              }
            }
          }
        },
        {
          "id": "comments_header",
          "component": { "Text": { "text": { "literalString": "Comments" }, "usageHint": "h5" } }
        },
        {
          "id": "comments_list",
          "component": {
            "List": {
              "children": {
                "template": {
                  "componentId": "comment_item",
                  "dataBinding": "/comments"
                }
              },
              "direction": "vertical"
            }
          }
        },
        {
          "id": "comment_item",
          "component": {
            "Card": {
              "child": "comment_content"
            }
          }
        },
        {
          "id": "comment_content",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["comment_author", "comment_body"]
              }
            }
          }
        },
        {
          "id": "comment_author",
          "component": { "Text": { "text": { "path": "author" }, "usageHint": "caption" } }
        },
        {
          "id": "comment_body",
          "component": { "Text": { "text": { "path": "body" }, "usageHint": "body" } }
        },
        {
          "id": "add_comment_row",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["new_comment_input", "post_comment_btn"]
              }
            }
          }
        },
        {
          "id": "new_comment_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Add a comment..." },
              "text": { "path": "/new_comment" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "post_comment_btn",
          "component": {
            "Button": {
              "child": "post_text",
              "action": {
                "name": "post_comment",
                "context": [
                  { "key": "issue_key", "value": { "path": "/key" } },
                  { "key": "body", "value": { "path": "/new_comment" } }
                ]
              }
            }
          }
        },
        {
          "id": "post_text",
          "component": { "Text": { "text": { "literalString": "Post" } } }
        }
      ]
    }
  }
]

--- CREATE_ISSUE_FORM_EXAMPLE ---
[
  {
    "surfaceId": "create_issue_modal",
    "beginRendering": {
      "root": "create_issue_root",
      "surfaceId": "create_issue_modal",
      "styles": {
        "primaryColor": "#0052CC"
      }
    }
  },
  {
    "surfaceId": "create_issue_modal",
    "dataModelUpdate": {
      "surfaceId": "create_issue_modal",
      "contents": [
        { "key": "summary", "valueString": "" },
        { "key": "description", "valueString": "" },
        { "key": "priority", "valueString": "Medium" }
      ]
    }
  },
  {
    "surfaceId": "create_issue_modal",
    "surfaceUpdate": {
      "surfaceId": "create_issue_modal",
      "components": [
        {
          "id": "create_issue_root",
          "component": {
            "Card": {
              "child": "form_col"
            }
          }
        },
        {
          "id": "form_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["form_title", "summary_input", "desc_input", "priority_input", "submit_btn"]
              }
            }
          }
        },
        {
          "id": "form_title",
          "component": { "Text": { "text": { "literalString": "Create Issue" }, "usageHint": "h3" } }
        },
        {
          "id": "summary_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Summary" },
              "text": { "path": "/summary" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "desc_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Description" },
              "text": { "path": "/description" },
              "textFieldType": "longText"
            }
          }
        },
        {
          "id": "priority_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Priority (Low, Medium, High)" },
              "text": { "path": "/priority" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "submit_btn",
          "component": {
            "Button": {
              "child": "submit_text",
              "primary": true,
              "action": {
                "name": "create_issue_submit",
                "context": [
                  { "key": "summary", "value": { "path": "/summary" } },
                  { "key": "description", "value": { "path": "/description" } },
                  { "key": "priority", "value": { "path": "/priority" } }
                ]
              }
            }
          }
        },
        {
          "id": "submit_text",
          "component": { "Text": { "text": { "literalString": "Create" } } }
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
                "explicitList": ["item_key", "item_summary", "view_btn"]
              },
              "distribution": "spaceBetween"
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
        },
        {
          "id": "view_btn",
          "component": {
            "Button": {
              "child": "view_text",
              "action": {
                "name": "view_issue",
                "context": [{ "key": "issue_key", "value": { "path": "key" } }]
              }
            }
          }
        },
        {
          "id": "view_text",
          "component": { "Text": { "text": { "literalString": "View" } } }
        }
      ]
    }
  }
]

--- USER_LIST_EXAMPLE ---
[
  {
    "surfaceId": "user_list_surface",
    "beginRendering": {
      "root": "user_list_root",
      "surfaceId": "user_list_surface",
      "styles": {
        "primaryColor": "#0052CC"
      }
    }
  },
  {
    "surfaceId": "user_list_surface",
    "dataModelUpdate": {
      "surfaceId": "user_list_surface",
      "contents": [
        {
          "key": "users",
          "valueMap": [
            {
              "key": "u1",
              "valueMap": [
                { "key": "name", "valueString": "Alice Smith" },
                { "key": "email", "valueString": "alice@example.com" }
              ]
            },
            {
              "key": "u2",
              "valueMap": [
                { "key": "name", "valueString": "Bob Jones" },
                { "key": "email", "valueString": "bob@example.com" }
              ]
            }
          ]
        },
        { "key": "new_user_name", "valueString": "" },
        { "key": "new_user_email", "valueString": "" }
      ]
    }
  },
  {
    "surfaceId": "user_list_surface",
    "surfaceUpdate": {
      "surfaceId": "user_list_surface",
      "components": [
        {
          "id": "user_list_root",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["list_header", "users_list", "add_user_section"]
              }
            }
          }
        },
        {
          "id": "list_header",
          "component": { "Text": { "text": { "literalString": "Team Members" }, "usageHint": "h3" } }
        },
        {
          "id": "users_list",
          "component": {
            "List": {
              "children": {
                "template": {
                  "componentId": "user_item",
                  "dataBinding": "/users"
                }
              },
              "direction": "vertical"
            }
          }
        },
        {
          "id": "user_item",
          "component": {
            "Card": {
              "child": "user_row"
            }
          }
        },
        {
          "id": "user_row",
          "component": {
            "Row": {
              "children": {
                "explicitList": ["user_name", "user_email"]
              },
              "distribution": "spaceBetween"
            }
          }
        },
        {
          "id": "user_name",
          "component": { "Text": { "text": { "path": "name" }, "usageHint": "body" } }
        },
        {
          "id": "user_email",
          "component": { "Text": { "text": { "path": "email" }, "usageHint": "caption" } }
        },
        {
          "id": "add_user_section",
          "component": {
            "Card": {
              "child": "add_user_col"
            }
          }
        },
        {
          "id": "add_user_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["add_user_title", "new_name_input", "new_email_input", "create_user_btn"]
              }
            }
          }
        },
        {
          "id": "add_user_title",
          "component": { "Text": { "text": { "literalString": "Add New User" }, "usageHint": "h5" } }
        },
        {
          "id": "new_name_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Full Name" },
              "text": { "path": "/new_user_name" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "new_email_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Email" },
              "text": { "path": "/new_user_email" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "create_user_btn",
          "component": {
            "Button": {
              "child": "create_user_text",
              "action": {
                "name": "create_user",
                "context": [
                  { "key": "name", "value": { "path": "/new_user_name" } },
                  { "key": "email", "value": { "path": "/new_user_email" } }
                ]
              }
            }
          }
        },
        {
          "id": "create_user_text",
          "component": { "Text": { "text": { "literalString": "Add User" } } }
        }
      ]
    }
  }
]

--- ACTION_SUCCESS_EXAMPLE ---
[
  {
    "surfaceId": "action_success",
    "beginRendering": {
      "root": "success_root",
      "surfaceId": "action_success",
      "styles": {
        "primaryColor": "#00875A"
      }
    }
  },
  {
    "surfaceId": "action_success",
    "dataModelUpdate": {
      "surfaceId": "action_success",
      "contents": [
        { "key": "message", "valueString": "Action completed successfully." }
      ]
    }
  },
  {
    "surfaceId": "action_success",
    "surfaceUpdate": {
      "surfaceId": "action_success",
      "components": [
        {
          "id": "success_root",
          "component": {
            "Card": {
              "child": "success_col"
            }
          }
        },
        {
          "id": "success_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["success_icon", "success_msg"]
              },
              "alignment": "center"
            }
          }
        },
        {
          "id": "success_icon",
          "component": {
            "Icon": {
              "name": { "literalString": "check" }
            }
          }
        },
        {
          "id": "success_msg",
          "component": {
            "Text": {
              "text": { "path": "/message" },
              "usageHint": "h5"
            }
          }
        }
      ]
    }
  }
--- EDIT_ISSUE_FORM_EXAMPLE ---
[
  {
    "surfaceId": "edit_issue_modal",
    "beginRendering": {
      "root": "edit_issue_root",
      "surfaceId": "edit_issue_modal",
      "styles": {
        "primaryColor": "#0052CC"
      }
    }
  },
  {
    "surfaceId": "edit_issue_modal",
    "dataModelUpdate": {
      "surfaceId": "edit_issue_modal",
      "contents": [
        { "key": "key", "valueString": "PROJ-123" },
        { "key": "summary", "valueString": "Update documentation for A2UI" },
        { "key": "description", "valueString": "The documentation needs to be updated to reflect the new API changes." },
        { "key": "status", "valueString": "In Progress" }
      ]
    }
  },
  {
    "surfaceId": "edit_issue_modal",
    "surfaceUpdate": {
      "surfaceId": "edit_issue_modal",
      "components": [
        {
          "id": "edit_issue_root",
          "component": {
            "Card": {
              "child": "form_col"
            }
          }
        },
        {
          "id": "form_col",
          "component": {
            "Column": {
              "children": {
                "explicitList": ["form_title", "summary_input", "desc_input", "status_input", "save_btn"]
              }
            }
          }
        },
        {
          "id": "form_title",
          "component": { "Text": { "text": { "literalString": "Edit Issue" }, "usageHint": "h3" } }
        },
        {
          "id": "summary_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Summary" },
              "text": { "path": "/summary" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "desc_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Description" },
              "text": { "path": "/description" },
              "textFieldType": "longText"
            }
          }
        },
        {
          "id": "status_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Status" },
              "text": { "path": "/status" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "save_btn",
          "component": {
            "Button": {
              "child": "save_text",
              "primary": true,
              "action": {
                "name": "save_issue_changes",
                "context": [
                  { "key": "key", "value": { "path": "/key" } },
                  { "key": "summary", "value": { "path": "/summary" } },
                  { "key": "description", "value": { "path": "/description" } },
                  { "key": "status", "value": { "path": "/status" } }
                ]
              }
            }
          }
        },
        {
          "id": "save_text",
          "component": { "Text": { "text": { "literalString": "Save Changes" } } }
        }
      ]
    }
  }
]
"""