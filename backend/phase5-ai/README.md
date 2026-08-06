# Phase 5 AI Backend

FastAPI bridge between the Network Security Lab and local Ollama inference.

## Endpoints

- `GET /health`
- `POST /chat`
- `POST /summarize`
- `POST /explain-log`
- `POST /explain-alert`
- `POST /explain-ospf`

Protected endpoints require:

Authorization: Bearer <API_TOKEN>
