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

SALESFORCE_UI_EXAMPLES = r"""
--- GENERIC_LIST_EXAMPLE ---
[
  {
    "surfaceId": "sf_list_surface",
    "beginRendering": {
      "root": "list_root",
      "surfaceId": "sf_list_surface",
      "styles": { "primaryColor": "#00A1E0" }
    }
  },
  {
    "surfaceId": "sf_list_surface",
    "dataModelUpdate": {
      "surfaceId": "sf_list_surface",
      "contents": [
        { "key": "title", "valueString": "Records" },
        {
          "key": "items",
          "valueMap": [
            {
              "key": "item1",
              "valueMap": [
                { "key": "id", "valueString": "001" },
                { "key": "title", "valueString": "Item Name" },
                { "key": "subtitle", "valueString": "Item Status" }
              ]
            }
          ]
        }
      ]
    }
  },
  {
    "surfaceId": "sf_list_surface",
    "surfaceUpdate": {
      "surfaceId": "sf_list_surface",
      "components": [
        {
          "id": "list_root",
          "component": {
            "Column": {
              "children": { "explicitList": ["header", "items_list"] }
            }
          }
        },
        {
          "id": "header",
          "component": { "Text": { "text": { "path": "title" }, "usageHint": "h3" } }
        },
        {
          "id": "items_list",
          "component": {
            "List": {
              "children": {
                "template": {
                  "componentId": "list_item",
                  "dataBinding": "/items"
                }
              },
              "direction": "vertical"
            }
          }
        },
        {
          "id": "list_item",
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
              "children": { "explicitList": ["item_info", "actions_row"] },
              "distribution": "spaceBetween",
              "alignment": "center"
            }
          }
        },
        {
          "id": "item_info",
          "component": {
            "Column": {
              "children": { "explicitList": ["item_title", "item_subtitle"] }
            }
          }
        },
        {
          "id": "item_title",
          "component": { "Text": { "text": { "path": "title" }, "usageHint": "h5" } }
        },
        {
          "id": "item_subtitle",
          "component": { "Text": { "text": { "path": "subtitle" }, "usageHint": "caption" } }
        },
        {
          "id": "actions_row",
          "component": {
            "Row": {
              "children": { "explicitList": ["view_btn"] }
            }
          }
        },
        {
          "id": "view_btn",
          "component": {
            "Button": {
              "child": "view_text",
              "action": {
                "name": "view_record",
                "context": [{ "key": "id", "value": { "path": "id" } }]
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

--- GENERIC_DETAIL_EXAMPLE ---
[
  {
    "surfaceId": "sf_detail_surface",
    "beginRendering": {
      "root": "detail_root",
      "surfaceId": "sf_detail_surface",
      "styles": { "primaryColor": "#00A1E0" }
    }
  },
  {
    "surfaceId": "sf_detail_surface",
    "dataModelUpdate": {
      "surfaceId": "sf_detail_surface",
      "contents": [
        { "key": "title", "valueString": "Record Details" },
        { "key": "id", "valueString": "001" },
        {
          "key": "fields",
          "valueMap": [
            {
              "key": "f1",
              "valueMap": [
                 { "key": "label", "valueString": "Status" },
                 { "key": "value", "valueString": "Active" }
              ]
            }
          ]
        }
      ]
    }
  },
  {
    "surfaceId": "sf_detail_surface",
    "surfaceUpdate": {
      "surfaceId": "sf_detail_surface",
      "components": [
        {
          "id": "detail_root",
          "component": {
            "Card": {
              "child": "content_col"
            }
          }
        },
        {
          "id": "content_col",
          "component": {
            "Column": {
              "children": { "explicitList": ["header_row", "divider", "fields_list", "actions_bar"] }
            }
          }
        },
        {
            "id": "header_row",
            "component": {
                "Row": {
                    "children": { "explicitList": ["title_text"] },
                    "distribution": "spaceBetween"
                }
            }
        },
        {
          "id": "title_text",
          "component": { "Text": { "text": { "path": "/title" }, "usageHint": "h3" } }
        },
        {
          "id": "divider",
          "component": { "Divider": { "axis": "horizontal" } }
        },
        {
          "id": "fields_list",
          "component": {
            "List": {
              "children": {
                "template": {
                  "componentId": "field_item",
                  "dataBinding": "/fields"
                }
              },
              "direction": "vertical"
            }
          }
        },
        {
          "id": "field_item",
          "component": {
            "Row": {
              "children": { "explicitList": ["field_label", "field_val"] },
              "distribution": "spaceBetween"
            }
          }
        },
        {
          "id": "field_label",
          "component": { "Text": { "text": { "path": "label" }, "usageHint": "caption" } }
        },
        {
          "id": "field_val",
          "component": { "Text": { "text": { "path": "value" }, "usageHint": "body" } }
        },
        {
            "id": "actions_bar",
            "component": {
                "Row": {
                    "children": { "explicitList": ["edit_btn", "delete_btn"] },
                    "distribution": "end"
                }
            }
        },
        {
            "id": "edit_btn",
            "component": {
                "Button": {
                    "child": "edit_txt",
                    "action": {
                        "name": "edit_record",
                        "context": [{ "key": "id", "value": { "path": "/id" } }]
                    }
                }
            }
        },
        { "id": "edit_txt", "component": { "Text": { "text": { "literalString": "Edit" } } } },
        {
            "id": "delete_btn",
            "component": {
                "Button": {
                    "child": "del_txt",
                    "action": {
                        "name": "delete_record",
                        "context": [{ "key": "id", "value": { "path": "/id" } }]
                    }
                }
            }
        },
        { "id": "del_txt", "component": { "Text": { "text": { "literalString": "Delete" }, "usageHint": "caption" } } }
      ]
    }
  }
]

--- CREATE_OPPORTUNITY_FORM ---
[
  {
    "surfaceId": "create_opp_surface",
    "beginRendering": {
      "root": "create_opp_root",
      "surfaceId": "create_opp_surface",
      "styles": { "primaryColor": "#00A1E0" }
    }
  },
  {
    "surfaceId": "create_opp_surface",
    "dataModelUpdate": {
      "surfaceId": "create_opp_surface",
      "contents": [
        { "key": "name", "valueString": "" },
        { "key": "amount", "valueString": "" },
        { "key": "stage", "valueString": "Prospecting" },
        { "key": "accountId", "valueString": "" }
      ]
    }
  },
  {
    "surfaceId": "create_opp_surface",
    "surfaceUpdate": {
      "surfaceId": "create_opp_surface",
      "components": [
        {
          "id": "create_opp_root",
          "component": { "Card": { "child": "form_col" } }
        },
        {
          "id": "form_col",
          "component": {
            "Column": {
              "children": { "explicitList": ["form_title", "name_input", "amount_input", "stage_input", "account_input", "submit_btn"] }
            }
          }
        },
        {
          "id": "form_title",
          "component": { "Text": { "text": { "literalString": "New Opportunity" }, "usageHint": "h3" } }
        },
        {
          "id": "name_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Opportunity Name" },
              "text": { "path": "/name" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "amount_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Amount" },
              "text": { "path": "/amount" },
              "textFieldType": "number"
            }
          }
        },
        {
          "id": "stage_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Stage" },
              "text": { "path": "/stage" },
              "textFieldType": "shortText"
            }
          }
        },
        {
          "id": "account_input",
          "component": {
            "TextField": {
              "label": { "literalString": "Account ID" },
              "text": { "path": "/accountId" },
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
                "name": "create_opportunity_submit",
                "context": [
                  { "key": "name", "value": { "path": "/name" } },
                  { "key": "amount", "value": { "path": "/amount" } },
                  { "key": "stage", "value": { "path": "/stage" } },
                  { "key": "accountId", "value": { "path": "/accountId" } }
                ]
              }
            }
          }
        },
        { "id": "submit_text", "component": { "Text": { "text": { "literalString": "Create Opportunity" } } } }
      ]
    }
  }
]
"""