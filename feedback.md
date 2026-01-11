# Workflow and Challenges Summary

This document outlines the workflow undertaken to configure and deploy the Orchestrator and Salesforce agents, along with the challenges encountered and their resolutions.

## Workflow Summary

The primary goal was to establish a deployment configuration for the multi-agent system and execute it. The workflow involved the following steps:

1.  **Containerization:** Created dedicated Dockerfiles (`Dockerfile.orchestrator` and `Dockerfile.salesforce`) for each agent to ensure their environments were properly defined.
2.  **Dependency Management:** The Orchestrator agent has a runtime dependency on the Salesforce agent. To manage this, the Orchestrator's startup logic (`__main__.py`) was modified to accept the Salesforce agent's URL via a `SUBAGENT_URLS` environment variable.
3.  **Deployment Automation:** The `deploy.sh` script was updated to orchestrate the deployment sequence:
    *   It first deploys the Salesforce agent to Google Cloud Run.
    *   It then captures the resulting service URL of the active Salesforce agent.
    *   Finally, it deploys the Orchestrator agent, injecting the captured Salesforce URL as the `SUBAGENT_URLS` environment variable.
4.  **Verification:** After deployment, the status of both services was checked using `gcloud` to ensure they were active and healthy.

## Challenges Encountered

The main challenge was an initial deployment failure of the Orchestrator agent.

*   **Problem:** The container would fail to start after being deployed.
*   **Root Cause Analysis:** Investigation revealed that `uvicorn`, the web server used to run the agent, was a necessary runtime dependency but was missing from the agent's `pyproject.toml` file.
*   **Resolution:** The missing `uvicorn` dependency was added to `pyproject.toml`, the `uv.lock` file was updated accordingly, and the agent was redeployed successfully.

## Deployment Connectivity and Resource Tuning - January 10, 2026

Following the initial deployment, runtime issues emerged related to service discovery and resource constraints.

### 1. Sub-Agent Service Discovery Fix
*   **Issue:** The Salesforce and Jira sub-agents were incorrectly reporting their internal container IP (`0.0.0.0`) in their Agent Cards instead of their public Cloud Run URLs. This prevented the Orchestrator from establishing connections to them.
*   **Resolution:**
    *   Modified `samples/agent/adk/adk_salesforce/__main__.py` and `samples/agent/adk/adk_jira/__main__.py` to respect an `AGENT_URL` environment variable.
    *   Redeployed both services (`adk-salesforce-service` and `adk-jira-service`) with the `AGENT_URL` variable set to their public HTTPS endpoints.

### 2. Orchestrator Stability Improvements
*   **Issue:** The Orchestrator service (`adk-orchestrator-service`) was crashing during startup with a "Memory limit of 512 MiB exceeded" error. Additionally, it failed startup health checks when it couldn't reach the sub-agents.
*   **Resolution:**
    *   Increased the Cloud Run memory limit for the Orchestrator service to **2Gi** (up from 512Mi).
    *   The service discovery fix (above) resolved the startup dependency timeout.
*   **Outcome:** All three services (Orchestrator, Salesforce, Jira) are now healthy and reachable, serving their Agent Cards correctly.