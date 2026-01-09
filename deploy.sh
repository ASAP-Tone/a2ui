#!/bin/bash
set -e

# Configuration
PROJECT="truiz-agent-builder"
REGION="us-central1"

echo "Creating deployment configuration..."
mkdir -p deploy

# Dockerfile for Jira
cat <<EOF > deploy/Dockerfile.jira
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY samples/agent/adk/pyproject.toml samples/agent/adk/uv.lock /app/samples/agent/adk/
COPY samples/agent/adk/adk_jira /app/samples/agent/adk/adk_jira
COPY a2a_agents/python/a2ui_extension /app/a2a_agents/python/a2ui_extension
WORKDIR /app/samples/agent/adk
RUN apt-get update && apt-get install -y git
RUN uv sync --package a2ui-adk-jira
WORKDIR /app/samples/agent/adk/adk_jira
ENV PORT=8080
CMD ["uv", "run", "__main__.py", "--host", "0.0.0.0", "--port", "8080"]
EOF

# Dockerfile for Salesforce
cat <<EOF > deploy/Dockerfile.salesforce
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY samples/agent/adk/pyproject.toml samples/agent/adk/uv.lock /app/samples/agent/adk/
COPY samples/agent/adk/adk_salesforce /app/samples/agent/adk/adk_salesforce
COPY a2a_agents/python/a2ui_extension /app/a2a_agents/python/a2ui_extension
WORKDIR /app/samples/agent/adk
RUN apt-get update && apt-get install -y git
RUN uv sync --package a2ui-adk-salesforce
WORKDIR /app/samples/agent/adk/adk_salesforce
ENV PORT=8080
CMD ["uv", "run", "__main__.py", "--host", "0.0.0.0", "--port", "8080"]
EOF

# echo "Deploying Jira Agent to Cloud Run..."
# cp deploy/Dockerfile.jira Dockerfile
# gcloud run deploy adk-jira-service \
#     --source . \
#     --project "$PROJECT" \
#     --region "$REGION" \
#     --allow-unauthenticated \
#     --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT"
# rm Dockerfile

echo "Deploying Salesforce Agent to Cloud Run..."
cp deploy/Dockerfile.salesforce Dockerfile
gcloud run deploy adk-salesforce-service \
    --source . \
    --project "$PROJECT" \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT"
rm Dockerfile

echo "Deployment complete!"
