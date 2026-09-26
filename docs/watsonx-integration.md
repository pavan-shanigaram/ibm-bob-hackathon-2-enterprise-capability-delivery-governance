# IBM watsonx.ai Integration Guide

## Overview

The platform integrates IBM watsonx.ai using the `ibm/granite-3-3-8b-instruct` foundation model
via the official `ibm-watsonx-ai` Python SDK to provide AI-powered governance intelligence.

## Setup

### 1. Create an IBM Cloud account
Visit [cloud.ibm.com](https://cloud.ibm.com) and sign up for a free account.

### 2. Create a watsonx.ai project
1. Go to [dataplatform.cloud.ibm.com](https://dataplatform.cloud.ibm.com)
2. Click "New project" → "Create an empty project"
3. Note your **Project ID** from the project settings

### 3. Generate an IBM Cloud API key
1. Go to [cloud.ibm.com/iam/apikeys](https://cloud.ibm.com/iam/apikeys)
2. Click "Create an IBM Cloud API key"
3. Copy the API key immediately (shown only once)

### 4. Configure environment variables
Edit your `.env` file:

```
WATSONX_API_KEY=your-ibm-cloud-api-key
WATSONX_PROJECT_ID=your-watsonx-project-id
WATSONX_URL=https://us-south.ml.cloud.ibm.com
WATSONX_MODEL_ID=ibm/granite-3-3-8b-instruct
```

### 5. Restart the backend
```bash
docker compose restart backend
```

### 6. Verify connectivity
```bash
curl http://localhost:8000/api/v1/ai/health
```

## AI Endpoints

| Endpoint | Input | Use Case |
|---|---|---|
| `POST /api/v1/ai/skill-gap-narrative` | `{"project_id": 1}` | Hiring & training recommendations |
| `POST /api/v1/ai/delivery-coach` | `{"squad_id": 1}` | Sprint improvement coaching |
| `POST /api/v1/ai/risk-summary` | (none) | Board-ready risk narrative |
| `GET /api/v1/ai/health` | — | Check connectivity |

## Graceful Fallback

If `WATSONX_API_KEY` is not configured, all AI endpoints return clearly labelled mock responses.
The platform is **fully functional** without watsonx credentials — this is by design for local development.

## Prompt Templates

### Skill Gap Narrative
```
You are an enterprise capability advisor. Given this project skill gap data: {data},
provide 3 specific hiring or training recommendations in bullet points.
```

### Delivery Coach
```
You are an agile delivery coach. Given these sprint metrics for squad '{name}': {metrics},
identify the top 2 delivery risks and suggest concrete improvements.
```

### Risk Summary
```
You are a CTO advisor. Summarize the following enterprise risk heatmap data: {heatmap}
in 3 sentences suitable for a board presentation.
```
