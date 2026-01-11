#!/bin/bash
set -e

# Configuration
PROJECT="truiz-agent-builder"
REGION="us-central1"

echo "Creating deployment configuration..."
mkdir -p deploy

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

# Dockerfile for Orchestrator
cat <<EOF > deploy/Dockerfile.orchestrator
FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim
WORKDIR /app
COPY samples/agent/adk/pyproject.toml samples/agent/adk/uv.lock /app/samples/agent/adk/
COPY samples/agent/adk/orchestrator /app/samples/agent/adk/orchestrator
COPY a2a_agents/python/a2ui_extension /app/a2a_agents/python/a2ui_extension
WORKDIR /app/samples/agent/adk
RUN apt-get update && apt-get install -y git
RUN uv sync --package orchestrator
WORKDIR /app/samples/agent/adk/orchestrator
ENV PORT=8080
CMD ["uv", "run", "__main__.py", "--host", "0.0.0.0", "--port", "8080"]
EOF

echo "Deploying Salesforce Agent to Cloud Run..."
cp deploy/Dockerfile.salesforce Dockerfile
gcloud run deploy adk-salesforce-service \
    --source . \
    --project "$PROJECT" \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT"
rm Dockerfile

# Get Salesforce URL
SALESFORCE_URL=$(gcloud run services describe adk-salesforce-service --project "$PROJECT" --region "$REGION" --format 'value(status.url)')
echo "Salesforce Agent URL: $SALESFORCE_URL"

echo "Deploying Orchestrator Agent to Cloud Run..."
cp deploy/Dockerfile.orchestrator Dockerfile
gcloud run deploy adk-orchestrator-service \
    --source . \
    --project "$PROJECT" \
    --region "$REGION" \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_GENAI_USE_VERTEXAI=TRUE,GOOGLE_CLOUD_PROJECT=$PROJECT,SUBAGENT_URLS=$SALESFORCE_URL"
rm Dockerfile

echo "Deployment complete!"
