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

import { cloneDefaultTheme } from "../theme/clone-default-theme.js";
import { AppConfig } from "./types.js";
import { v0_8 } from "@a2ui/lit";

const theme: v0_8.Types.Theme = {
  ...cloneDefaultTheme(),
  additionalStyles: {
    Card: {
      "min-width": "320px",
      "max-width": "400px",
      margin: "0 auto",
      background:
        "linear-gradient(135deg, light-dark(#ffffff99, #ffffff44) 0%, light-dark(#ffffff, #ffffff04) 100%)",
      border: "1px solid light-dark(transparent, #ffffff35)",
      boxShadow:
        "inset 0 20px 48px light-dark(rgba(0, 0, 0, 0.02), rgba(255, 255, 255, 0.08))",
    },
  },
};

export const config: AppConfig = {
  key: "jira",
  title: "Jira Assistant",
  background: `linear-gradient(135deg, #0052CC 0%, #2684FF 100%)`, 
  placeholder: "Show me details for PROJ-123",
  loadingText: [
    "Connecting to Jira...",
    "Fetching issues...",
    "Processing request...",
  ],
  serverUrl: "http://localhost:10002",
  theme,
};
