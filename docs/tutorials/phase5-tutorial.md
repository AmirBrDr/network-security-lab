# Phase 5 - Local AI Infrastructure With Ollama And FastAPI

Network Security Lab

## Summary

This practical lab connects the network security lab to a local AI inference
machine. The MacBook Pro runs Ollama and stores the local models. The
Management VM runs a small FastAPI backend that exposes controlled API
endpoints for chat, summarization, log explanation, alert explanation, and
basic OSPF failure explanation.

The AI layer is intentionally a support layer:

- The OSPF, observability, and security evidence remains the source of truth.
- Ollama runs locally on the MacBook Pro M3 Pro with 18 GB RAM.
- The university server keeps running the lab VMs and does not need a GPU.
- FastAPI is the bridge between lab data and the local model.
- Loki and Prometheus provide the evidence used by the backend.
- API access is restricted with a simple bearer token and controlled network
  exposure.

At the end of this lab, the Management VM must be able to send a lab event to
the FastAPI backend, the backend must query Ollama on the Mac, and the response
must include a cautious explanation based on supplied evidence.

## Table Of Contents

1. Objectives
2. Lab Topology
3. AI Safety And Scope
4. Service And Model Plan
5. Prepare The MacBook Pro
6. Install And Verify Ollama
7. Pull The Lab Models
8. Validate The Ollama API Locally
9. Benchmark Models
10. Expose Ollama To The Lab Safely
11. Validate Mac To Management Connectivity
12. Prepare The Management VM
13. Create The FastAPI Backend
14. Configure The Backend Environment
15. Add API Authentication
16. Add Ollama Client Functions
17. Add Loki And Prometheus Client Functions
18. Add Health, Chat, And Summarization Endpoints
19. Add Log And Alert Explanation Endpoints
20. Add OSPF Failure Explanation Endpoint
21. Run The Backend Manually
22. Install The Backend As A systemd Service
23. Validate The End To End AI Flow
24. Add Observability For The Backend
25. Save Evidence
26. Troubleshooting
27. Conclusion
28. References

## 1. Objectives

After completing this practical lab, you should be able to:

1. Install or verify Ollama on the MacBook Pro.
2. Pull and test the project models from `docs/ai-stack.md`.
3. Benchmark local model behavior for diagnostic, fast, code, and embedding
   tasks.
4. Expose Ollama only to the controlled lab path.
5. Validate connectivity from the Management VM to the Mac.
6. Create a FastAPI backend on the Management VM.
7. Protect the backend with a simple bearer token.
8. Connect FastAPI to Ollama, Loki, and Prometheus.
9. Add endpoints for `health`, `chat`, `summarize`, `explain-log`,
   `explain-alert`, and `explain-ospf`.
10. Add timeout, fallback, and missing-evidence behavior.
11. Install the backend as a persistent service.
12. Prove one full event-to-AI explanation flow.

## 2. Lab Topology

Phase 5 starts after the routing, observability, and security layers:

- Phase 1 provides the OSPFv2/OSPFv3 topology.
- Phase 2 provides controlled network failure evidence.
- Phase 3 provides Prometheus, Loki, Grafana, and FRR metrics.
- Phase 4 provides Suricata IDS alerts and incident evidence.

The MacBook Pro is not a router and is not part of OSPF. It is an external AI
inference endpoint used by the Management VM.

```text
                      MacBook Pro M3 Pro
                      Ollama :11434
                             ^
                             |
                  controlled API path
                             |
                             v
 Management VM 10.99.0.66 ---+--- FastAPI :8080
   Prometheus :9090               Loki :3100
   Grafana :3000                  AI backend

        Management VLAN 99
 R1 10.99.0.1  R2 10.99.0.2  R3 10.99.0.3  monitoring 10.99.0.65
```

Recommended service placement:

| Component | Host | Port | Purpose |
| --- | --- | ---: | --- |
| Ollama | MacBook Pro | `11434/tcp` | Local model inference |
| FastAPI backend | Management VM | `8080/tcp` | Lab AI API |
| Prometheus | Management VM | `9090/tcp` | Metrics evidence |
| Loki | Management VM | `3100/tcp` | Logs and alert evidence |
| Grafana | Management VM | `3000/tcp` | Dashboards and screenshots |

The backend should be reachable from the Management VM and, later, the demo UI.
It should not be exposed publicly.

## 3. AI Safety And Scope

Q1. What should the AI layer be allowed to do?

The Phase 5 backend is read-only. It may:

- Summarize text supplied by the user.
- Explain logs supplied by the user.
- Query Loki for recent logs.
- Query Prometheus for selected metrics.
- Ask Ollama for a cautious explanation.
- Return suggested verification commands.

It must not:

- Run commands on routers.
- Change FRR, OVS, Netplan, Suricata, Grafana, or Prometheus configuration.
- Launch scans or security tests.
- Claim certainty when evidence is incomplete.
- Send lab evidence to a cloud model.

Q2. What is the privacy boundary?

Ollama must run locally. The backend should call only:

- `http://<mac-ip>:11434`
- `http://127.0.0.1:9090`
- `http://127.0.0.1:3100`

Do not send private logs, packet captures, SSH keys, tokens, or credentials to
external APIs.

Q3. How should AI answers be phrased?

Every explanation should separate:

- Observed evidence
- Likely interpretation
- Missing data
- Suggested verification

This keeps the assistant useful without letting it pretend that a guess is a
fact.

## 4. Service And Model Plan

Q4. Which models does the project plan to use?

`docs/ai-stack.md` defines the initial model plan:

| Use case | Model |
| --- | --- |
| Default diagnostic model | `qwen2.5:14b` |
| Fast fallback | `llama3.1:8b` |
| Code and configuration help | `qwen2.5-coder:14b` |
| Embeddings | `nomic-embed-text` |

Q5. Why keep these models even if newer models exist?

The goal of Phase 5 is a stable local AI infrastructure, not model chasing.
The selected models are practical for an 18 GB MacBook Pro and already match
the repository plan.

Optional note for later:

- If `qwen3`, `qwen3-embedding`, or another newer model performs better on the
  same hardware, evaluate it in the benchmark table before changing the default
  stack.
- Record any model change in `docs/ai-stack.md` and the Phase 5 proof report.

Q6. What are the expected model roles?

| Model | Expected role | Success criterion |
| --- | --- | --- |
| `qwen2.5:14b` | Main network/security diagnostic explanations | Clear, cautious answers with useful commands |
| `llama3.1:8b` | Fast fallback when latency matters | Short summaries with lower latency |
| `qwen2.5-coder:14b` | FRR, YAML, Python, and shell explanation | Better code/config reasoning |
| `nomic-embed-text` | Embedding smoke test for later RAG | Returns numeric vectors through `/api/embed` |

## 5. Prepare The MacBook Pro

Q7. Which Mac resource checks should be captured?

Run on the Mac:

```console
sw_vers
uname -m
sysctl -n machdep.cpu.brand_string
sysctl hw.memsize
df -h
```

Expected result:

- Architecture is Apple Silicon, usually `arm64`.
- Memory is around 18 GB.
- Disk has enough free space for several model files.

Q8. Which network information should be recorded?

Run on the Mac:

```console
hostname
ipconfig getifaddr en0 2>/dev/null || true
ifconfig en0 | grep "inet "
```

If the Mac uses another interface, such as Ethernet or VPN, replace `en0`.

Record:

| Field | Value |
| --- | --- |
| Mac hostname | `<mac-hostname>` |
| Mac LAN or VPN IPv4 | `<mac-ip>` |
| Ollama URL from Management VM | `http://<mac-ip>:11434` |

Q9. What firewall decision is recommended?

Allow inbound access to Ollama only from the Management VM or the controlled
server path. If the Mac firewall is enabled, create the narrowest rule possible
for the lab. Do not expose `11434/tcp` on public Wi-Fi.

Q10. Which helper tools are useful on the Mac?

Several validation commands use `jq`. Install it if it is missing:

```console
command -v jq >/dev/null 2>&1 || brew install jq
```

## 6. Install And Verify Ollama

Q11. How do we install Ollama on macOS?

Install from the official Ollama download page, or use Homebrew if that is how
the Mac is managed.

Official app path:

```text
https://ollama.com/download
```

Homebrew option:

```console
brew install ollama
```

Q12. How do we verify the CLI?

```console
ollama --version
ollama list
```

Expected result:

- `ollama --version` prints the installed version.
- `ollama list` prints either an empty model list or existing models.

Q13. How do we verify the local API?

Ollama serves its local API on port `11434` by default.

```console
curl -s http://127.0.0.1:11434/api/version | jq
curl -s http://127.0.0.1:11434/api/tags | jq
```

Expected result:

- `/api/version` returns JSON with the Ollama version.
- `/api/tags` returns the local model list.

## 7. Pull The Lab Models

Q14. How do we pull the default diagnostic model?

```console
ollama pull qwen2.5:14b
```

Q15. How do we pull the fast fallback model?

```console
ollama pull llama3.1:8b
```

Q16. How do we pull the code model?

```console
ollama pull qwen2.5-coder:14b
```

Q17. How do we pull the embedding model?

```console
ollama pull nomic-embed-text
```

Q18. How do we verify local model inventory?

```console
ollama list
```

Expected result:

```text
qwen2.5:14b
llama3.1:8b
qwen2.5-coder:14b
nomic-embed-text
```

The exact IDs, sizes, and timestamps can differ.

## 8. Validate The Ollama API Locally

Q19. How do we test `/api/chat`?

On the Mac:

```console
curl -s http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen2.5:14b",
    "stream": false,
    "messages": [
      {
        "role": "system",
        "content": "You are a cautious network security lab assistant. Answer only from supplied evidence."
      },
      {
        "role": "user",
        "content": "Explain in one paragraph what an OSPF neighbor loss alert usually means."
      }
    ]
  }' | jq
```

Expected result:

- JSON is returned.
- The response contains a short explanation.
- No streaming chunks appear because `stream` is set to `false`.

Q20. How do we test `/api/generate`?

```console
curl -s http://127.0.0.1:11434/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "stream": false,
    "prompt": "Summarize this event: R2 has fewer than two Full OSPFv2 neighbors."
  }' | jq
```

Expected result:

- The response includes a `response` field.
- The answer is shorter and faster than the default model in most cases.

Q21. How do we test `/api/embed`?

```console
curl -s http://127.0.0.1:11434/api/embed \
  -H "Content-Type: application/json" \
  -d '{
    "model": "nomic-embed-text",
    "input": "OSPF adjacency changed from Full to Deleted on VLAN 440."
  }' | jq '.model, (.embeddings[0] | length)'
```

Expected result:

- The model name is returned.
- The embedding length is a positive integer.

Q22. How do we preload a model for faster tests?

```console
curl -s http://127.0.0.1:11434/api/chat \
  -H "Content-Type: application/json" \
  -d '{"model":"qwen2.5:14b","messages":[]}' | jq
ollama ps
```

Expected result:

- The model appears in `ollama ps`.
- Later requests avoid the first-load delay while the model remains loaded.

## 9. Benchmark Models

Q23. Why benchmark locally?

The MacBook Pro has limited memory compared with a dedicated GPU server.
Benchmarks help choose the default model based on useful behavior, not only
model size.

Q24. What prompts should be used?

Use three fixed prompts:

```text
Prompt A - OSPF diagnostic:
Evidence:
- Router: R2
- Alert: OSPFNeighborLoss
- Metric: frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"} = 1
- Log: Full -> Deleted on enp0s1.440
Explain the likely cause, missing evidence, and next verification commands.
```

```text
Prompt B - Suricata incident:
Evidence:
- Signature: LOCAL Phase4 TCP SYN scan candidate
- Source: 10.20.0.156
- Destination: 10.10.0.169
- Time window: last 5 minutes
Summarize the incident and propose response steps.
```

```text
Prompt C - Config help:
Explain this PromQL expression and what it detects:
frr_ospf_neighbor_full_total < 2
```

Q25. How do we run a simple benchmark from the Mac?

Create a temporary benchmark script:

```console
mkdir -p ~/network-security-lab-ai-bench
cd ~/network-security-lab-ai-bench

cat > benchmark-ollama.sh <<'EOF'
#!/bin/sh
set -eu

MODELS="qwen2.5:14b llama3.1:8b qwen2.5-coder:14b"
PROMPT='Evidence:
- Router: R2
- Alert: OSPFNeighborLoss
- Metric: frr_ospf_neighbor_full_total{node="R2",protocol="ospfv2"} = 1
- Log: Full -> Deleted on enp0s1.440
Explain the likely cause, missing evidence, and next verification commands.'

for model in $MODELS; do
  echo "===== $model ====="
  START="$(date +%s)"
  curl -s http://127.0.0.1:11434/api/chat \
    -H "Content-Type: application/json" \
    -d "$(jq -n --arg model "$model" --arg prompt "$PROMPT" '{
      model: $model,
      stream: false,
      options: {temperature: 0.2, num_ctx: 4096},
      messages: [
        {role: "system", content: "You are a cautious network security lab assistant. Separate evidence, interpretation, missing data, and verification commands."},
        {role: "user", content: $prompt}
      ]
    }')" \
    | jq -r '.message.content // .response // .error'
  END="$(date +%s)"
  echo "duration_seconds=$((END - START))"
done
EOF

chmod +x benchmark-ollama.sh
./benchmark-ollama.sh | tee benchmark-results.txt
```

Q26. What should be recorded?

| Model | Prompt | Duration | Quality notes | Selected role |
| --- | --- | ---: | --- | --- |
| `qwen2.5:14b` | OSPF diagnostic | `<seconds>` | `<notes>` | Default |
| `llama3.1:8b` | OSPF diagnostic | `<seconds>` | `<notes>` | Fast fallback |
| `qwen2.5-coder:14b` | Config help | `<seconds>` | `<notes>` | Code/config |
| `nomic-embed-text` | Embedding smoke test | `<seconds>` | `<dimension>` | RAG preparation |

Q27. What selection rule should be used?

Use:

- `qwen2.5:14b` for normal explanations if latency is acceptable.
- `llama3.1:8b` if the default model is too slow or not loaded.
- `qwen2.5-coder:14b` for code, YAML, shell, and FRR configuration questions.
- `nomic-embed-text` only for embeddings, not chat.

## 10. Expose Ollama To The Lab Safely

Q28. What is the safest first connection method?

Use SSH port forwarding first. It avoids exposing Ollama to the network while
you validate the backend.

From the Management VM or from a machine that can SSH to the Mac:

```console
ssh -N -L 11434:127.0.0.1:11434 <mac-user>@<mac-ip>
```

Then test from the Management VM:

```console
curl -s http://127.0.0.1:11434/api/version | jq
```

Expected result:

- The Management VM reaches Ollama through the local tunnel.
- No Mac firewall change is required for this first test.

Q29. How can Ollama be exposed directly to the controlled lab path?

If direct access is required, configure Ollama on macOS to listen on a
non-loopback address:

```console
launchctl setenv OLLAMA_HOST "0.0.0.0:11434"
```

Restart the Ollama application after setting the environment variable.

Then verify on the Mac:

```console
curl -s http://127.0.0.1:11434/api/version | jq
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

Q30. What firewall check is required?

From the Management VM:

```console
MAC_OLLAMA_URL="http://<mac-ip>:11434"
curl -s "$MAC_OLLAMA_URL/api/version" | jq
```

Expected result:

- The request succeeds only from the controlled lab path.
- The Mac does not expose Ollama on untrusted networks.

Q31. How do we disable direct exposure later?

On the Mac:

```console
launchctl unsetenv OLLAMA_HOST
```

Restart Ollama and verify it is bound only to localhost:

```console
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

## 11. Validate Mac To Management Connectivity

Q32. Which direction should be tested?

The important Phase 5 path is:

```text
Management VM -> MacBook Pro Ollama API
```

Q33. What should be tested from the Management VM?

```console
MAC_OLLAMA_URL="http://<mac-ip>:11434"

ping -c 3 <mac-ip>
nc -vz <mac-ip> 11434
curl -s "$MAC_OLLAMA_URL/api/version" | jq
curl -s "$MAC_OLLAMA_URL/api/tags" | jq '.models[].name'
```

Expected result:

- ICMP may succeed or fail depending on firewall settings.
- TCP port `11434` must succeed if direct exposure is used.
- `/api/version` and `/api/tags` return JSON.

Q34. How do we test an actual remote inference request?

```console
curl -s "$MAC_OLLAMA_URL/api/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama3.1:8b",
    "stream": false,
    "messages": [
      {"role": "user", "content": "Reply with exactly: phase5 remote ollama ok"}
    ]
  }' | jq -r '.message.content'
```

Expected result:

```text
phase5 remote ollama ok
```

Small wording differences are acceptable, but exact output is better evidence.

## 12. Prepare The Management VM

Q35. Why run the backend on the Management VM?

The Management VM already has local access to:

- Prometheus at `127.0.0.1:9090`
- Loki at `127.0.0.1:3100`
- Grafana at `127.0.0.1:3000`
- Lab management network `10.99.0.0/24`

It is the natural bridge between lab evidence and the Mac model endpoint.

Q36. Which packages are needed?

Run on the Management VM:

```console
sudo apt update
sudo apt install -y python3 python3-venv python3-pip curl jq git moreutils
```

Q37. Which directory layout should be used?

Use the existing `backend/` folder in the repository:

```text
backend/
  phase5-ai/
    app/
      __init__.py
      main.py
    requirements.txt
    .env.example
    README.md
```

Create the directory:

```console
cd /path/to/network-security-lab
mkdir -p backend/phase5-ai/app
```

Replace `/path/to/network-security-lab` with the actual repository path on the
Management VM.

## 13. Create The FastAPI Backend

Q38. How do we create the Python environment?

On the Management VM:

```console
cd /path/to/network-security-lab/backend/phase5-ai
python3 -m venv .venv
. .venv/bin/activate
python -m pip install --upgrade pip
```

Q39. Which Python dependencies are required?

Create `requirements.txt`:

```console
cat > requirements.txt <<'EOF'
fastapi
uvicorn[standard]
httpx
pydantic-settings
python-dotenv
EOF

python -m pip install -r requirements.txt
```

Q40. What is the smallest useful FastAPI app?

Create `app/__init__.py`:

```console
touch app/__init__.py
```

Create `app/main.py`:

```console
cat > app/main.py <<'EOF'
from __future__ import annotations

import time
from functools import lru_cache
from typing import Any

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "network-security-lab-ai"
    api_token: str
    ollama_url: str = "http://127.0.0.1:11434"
    default_model: str = "qwen2.5:14b"
    fast_model: str = "llama3.1:8b"
    code_model: str = "qwen2.5-coder:14b"
    embedding_model: str = "nomic-embed-text"
    prometheus_url: str = "http://127.0.0.1:9090"
    loki_url: str = "http://127.0.0.1:3100"
    request_timeout_seconds: float = 45.0


@lru_cache
def get_settings() -> Settings:
    return Settings()


def require_token(
    authorization: str | None = Header(default=None),
    settings: Settings = Depends(get_settings),
) -> None:
    expected = f"Bearer {settings.api_token}"
    if authorization != expected:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid bearer token",
        )


class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=8000)
    model: str | None = None
    use_fast_model: bool = False


class SummarizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=12000)
    model: str | None = None


class ExplainLogRequest(BaseModel):
    log_text: str = Field(min_length=1, max_length=12000)
    model: str | None = None


class ExplainAlertRequest(BaseModel):
    alert_name: str = Field(min_length=1, max_length=200)
    labels: dict[str, Any] = Field(default_factory=dict)
    annotations: dict[str, Any] = Field(default_factory=dict)
    model: str | None = None


class ExplainOspfRequest(BaseModel):
    node: str = Field(default="R2", max_length=40)
    protocol: str = Field(default="ospfv2", max_length=20)
    lookback_minutes: int = Field(default=15, ge=1, le=180)
    model: str | None = None


app = FastAPI(title="Network Security Lab AI Backend", version="0.1.0")


async def ollama_chat(settings: Settings, model: str, user_prompt: str) -> str:
    payload = {
        "model": model,
        "stream": False,
        "options": {"temperature": 0.2, "num_ctx": 4096},
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are a cautious network security lab assistant. "
                    "Use only supplied evidence. Separate observed evidence, "
                    "likely interpretation, missing data, and verification commands."
                ),
            },
            {"role": "user", "content": user_prompt},
        ],
    }
    timeout = httpx.Timeout(settings.request_timeout_seconds)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.post(f"{settings.ollama_url}/api/chat", json=payload)
        response.raise_for_status()
        data = response.json()
    return data.get("message", {}).get("content", "")


async def prometheus_query(settings: Settings, query: str) -> dict[str, Any]:
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            f"{settings.prometheus_url}/api/v1/query",
            params={"query": query},
        )
        response.raise_for_status()
        return response.json()


async def loki_query_range(settings: Settings, query: str, minutes: int) -> dict[str, Any]:
    now_ns = int(time.time() * 1_000_000_000)
    start_ns = now_ns - minutes * 60 * 1_000_000_000
    timeout = httpx.Timeout(10.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        response = await client.get(
            f"{settings.loki_url}/loki/api/v1/query_range",
            params={"query": query, "start": start_ns, "end": now_ns, "limit": 30},
        )
        response.raise_for_status()
        return response.json()


@app.get("/health")
async def health(settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    checks: dict[str, Any] = {"app": "ok"}
    timeout = httpx.Timeout(5.0)
    async with httpx.AsyncClient(timeout=timeout) as client:
        for name, url in {
            "ollama": f"{settings.ollama_url}/api/version",
            "prometheus": f"{settings.prometheus_url}/-/ready",
            "loki": f"{settings.loki_url}/ready",
        }.items():
            try:
                response = await client.get(url)
                checks[name] = {
                    "ok": response.status_code < 400,
                    "status_code": response.status_code,
                }
            except Exception as exc:
                checks[name] = {"ok": False, "error": str(exc)}
    return checks


@app.post("/chat", dependencies=[Depends(require_token)])
async def chat(req: ChatRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    model = req.model or (settings.fast_model if req.use_fast_model else settings.default_model)
    answer = await ollama_chat(settings, model, req.message)
    return {"model": model, "answer": answer}


@app.post("/summarize", dependencies=[Depends(require_token)])
async def summarize(req: SummarizeRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    model = req.model or settings.fast_model
    prompt = f"Summarize this lab evidence in concise incident-note style:\n\n{req.text}"
    answer = await ollama_chat(settings, model, prompt)
    return {"model": model, "answer": answer}


@app.post("/explain-log", dependencies=[Depends(require_token)])
async def explain_log(req: ExplainLogRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    model = req.model or settings.default_model
    prompt = f"Explain this log entry. Include missing evidence and verification commands:\n\n{req.log_text}"
    answer = await ollama_chat(settings, model, prompt)
    return {"model": model, "answer": answer}


@app.post("/explain-alert", dependencies=[Depends(require_token)])
async def explain_alert(req: ExplainAlertRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    model = req.model or settings.default_model
    prompt = (
        "Explain this alert from the network security lab.\n"
        f"Alert: {req.alert_name}\n"
        f"Labels: {req.labels}\n"
        f"Annotations: {req.annotations}\n"
    )
    answer = await ollama_chat(settings, model, prompt)
    return {"model": model, "answer": answer}


@app.post("/explain-ospf", dependencies=[Depends(require_token)])
async def explain_ospf(req: ExplainOspfRequest, settings: Settings = Depends(get_settings)) -> dict[str, Any]:
    model = req.model or settings.default_model
    metric_query = f'frr_ospf_neighbor_full_total{{node="{req.node}",protocol="{req.protocol}"}}'
    log_query = '{job="systemd-journal", unit="frr.service"} |= "AdjChg"'

    metric_data: dict[str, Any]
    log_data: dict[str, Any]
    try:
        metric_data = await prometheus_query(settings, metric_query)
    except Exception as exc:
        metric_data = {"error": str(exc)}
    try:
        log_data = await loki_query_range(settings, log_query, req.lookback_minutes)
    except Exception as exc:
        log_data = {"error": str(exc)}

    prompt = (
        "Explain this OSPF situation using only the supplied evidence.\n"
        f"Node: {req.node}\n"
        f"Protocol: {req.protocol}\n"
        f"Prometheus query: {metric_query}\n"
        f"Prometheus result: {metric_data}\n"
        f"Loki query: {log_query}\n"
        f"Loki result: {log_data}\n"
        "Return sections: observed evidence, likely interpretation, missing data, verification commands."
    )
    answer = await ollama_chat(settings, model, prompt)
    return {
        "model": model,
        "prometheus_query": metric_query,
        "loki_query": log_query,
        "answer": answer,
    }
EOF
```

This single file is enough for Phase 5. Later phases can split clients,
schemas, and routes into separate modules.

## 14. Configure The Backend Environment

Q41. Which environment variables are required?

Create `.env.example`:

```console
cat > .env.example <<'EOF'
API_TOKEN=change-me
OLLAMA_URL=http://<mac-ip>:11434
DEFAULT_MODEL=qwen2.5:14b
FAST_MODEL=llama3.1:8b
CODE_MODEL=qwen2.5-coder:14b
EMBEDDING_MODEL=nomic-embed-text
PROMETHEUS_URL=http://127.0.0.1:9090
LOKI_URL=http://127.0.0.1:3100
REQUEST_TIMEOUT_SECONDS=45
EOF
```

Create the real `.env` file:

```console
cp .env.example .env
python - <<'PY'
import secrets
print("API_TOKEN=" + secrets.token_urlsafe(32))
PY
```

Edit `.env`:

```dotenv
API_TOKEN=<generated-token>
OLLAMA_URL=http://<mac-ip>:11434
DEFAULT_MODEL=qwen2.5:14b
FAST_MODEL=llama3.1:8b
CODE_MODEL=qwen2.5-coder:14b
EMBEDDING_MODEL=nomic-embed-text
PROMETHEUS_URL=http://127.0.0.1:9090
LOKI_URL=http://127.0.0.1:3100
REQUEST_TIMEOUT_SECONDS=45
```

Do not commit `.env`.

Q42. How do we document the backend locally?

Create `README.md` inside `backend/phase5-ai/`:

```console
cat > README.md <<'EOF'
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
EOF
```

## 15. Add API Authentication

Q43. How is authentication implemented?

The tutorial app checks the `Authorization` header:

```text
Authorization: Bearer <API_TOKEN>
```

This is not enterprise identity management. It is a simple lab protection so
that the backend is not an open prompt relay.

Q44. How do we test a missing token?

```console
curl -s -X POST http://127.0.0.1:8080/chat \
  -H "Content-Type: application/json" \
  -d '{"message":"hello"}' | jq
```

Expected result:

```json
{
  "detail": "Missing or invalid bearer token"
}
```

Q45. How do we test a valid token?

```console
export API_TOKEN="$(grep '^API_TOKEN=' .env | cut -d= -f2-)"

curl -s -X POST http://127.0.0.1:8080/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"message":"Reply with exactly: phase5 backend auth ok","use_fast_model":true}' | jq
```

Expected result:

- The backend returns a model name and answer.
- The answer should confirm the test phrase.

## 16. Add Ollama Client Functions

Q46. Which Ollama endpoint does the backend use for normal answers?

The backend uses:

```text
POST /api/chat
```

It sends:

- `model`
- `stream: false`
- `options.temperature`
- `options.num_ctx`
- `messages`

Q47. Why set `stream` to `false`?

It simplifies the first backend implementation. Streaming can be added in the
demo phase, but Phase 5 should first prove reliable request/response behavior.

Q48. How do we test Ollama through FastAPI?

Run on the Management VM after starting the backend:

```console
export API_TOKEN="$(grep '^API_TOKEN=' .env | cut -d= -f2-)"

curl -s -X POST http://127.0.0.1:8080/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "message": "Explain why AI answers must cite evidence in a network incident report.",
    "use_fast_model": true
  }' | jq -r '.answer'
```

Expected result:

- The answer arrives through the backend.
- It does not require direct shell access to the Mac.

## 17. Add Loki And Prometheus Client Functions

Q49. Which Prometheus query proves Phase 3 data is reachable?

```console
curl -s "http://127.0.0.1:9090/api/v1/query" \
  --data-urlencode 'query=frr_ospf_neighbor_full_total' | jq
```

Expected result:

- Prometheus returns OSPF neighbor metrics for `R1`, `R2`, and `R3`.

Q50. Which Loki query proves log data is reachable?

```console
curl -G -s "http://127.0.0.1:3100/loki/api/v1/query_range" \
  --data-urlencode 'query={job="systemd-journal", unit="frr.service"} |= "AdjChg"' \
  --data-urlencode 'limit=5' | jq
```

Expected result:

- Loki returns FRR adjacency logs if they exist in the current time range.
- Empty results are acceptable if no recent adjacency event exists.

Q51. Why does the backend catch Prometheus and Loki errors?

The AI backend should not crash just because one evidence source is empty or
temporarily unavailable. It should return:

- The evidence it could collect.
- The error for the unavailable source.
- A response that says evidence is missing.

## 18. Add Health, Chat, And Summarization Endpoints

Q52. How do we test `GET /health`?

```console
curl -s http://127.0.0.1:8080/health | jq
```

Expected result:

```json
{
  "app": "ok",
  "ollama": {
    "ok": true
  },
  "prometheus": {
    "ok": true
  },
  "loki": {
    "ok": true
  }
}
```

Exact fields can include HTTP status codes.

Q53. How do we test `POST /chat`?

```console
export API_TOKEN="$(grep '^API_TOKEN=' .env | cut -d= -f2-)"

curl -s -X POST http://127.0.0.1:8080/chat \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "message": "Give three verification commands for an OSPF neighbor loss.",
    "use_fast_model": true
  }' | jq
```

Q54. How do we test `POST /summarize`?

```console
curl -s -X POST http://127.0.0.1:8080/summarize \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "text": "R2 reported OSPFNeighborLoss. The FRR log shows Full -> Deleted on enp0s1.440. Prometheus shows one full OSPFv2 neighbor instead of two."
  }' | jq -r '.answer'
```

Expected result:

- The response summarizes the incident.
- It does not invent a final root cause unless supplied evidence supports it.

## 19. Add Log And Alert Explanation Endpoints

Q55. How do we test `POST /explain-log`?

```console
curl -s -X POST http://127.0.0.1:8080/explain-log \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "log_text": "R2 frr[1234]: AdjChg: Nbr 1.0.0.4 on enp0s1.440: Full -> Deleted"
  }' | jq -r '.answer'
```

Expected result:

- The answer identifies an OSPF adjacency loss.
- It suggests checking interface state, VLAN `440`, FRR neighbors, and Loki or
  Prometheus evidence.

Q56. How do we test `POST /explain-alert`?

```console
curl -s -X POST http://127.0.0.1:8080/explain-alert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "alert_name": "SuricataAlertObserved",
    "labels": {
      "node": "monitoring",
      "phase": "phase-4-security",
      "severity": "info"
    },
    "annotations": {
      "summary": "Suricata alert observed on monitoring",
      "description": "Suricata recorded at least one alert in the last five minutes."
    }
  }' | jq -r '.answer'
```

Expected result:

- The answer explains what the alert means.
- It asks for Suricata signature, source IP, destination IP, and time window if
  those are missing.

## 20. Add OSPF Failure Explanation Endpoint

Q57. What does `POST /explain-ospf` do?

It queries:

- Prometheus for `frr_ospf_neighbor_full_total`
- Loki for recent FRR adjacency changes
- Ollama for a cautious explanation using both results

Q58. How do we test the endpoint at healthy baseline?

```console
curl -s -X POST http://127.0.0.1:8080/explain-ospf \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "node": "R2",
    "protocol": "ospfv2",
    "lookback_minutes": 30
  }' | jq -r '.answer'
```

Expected healthy result:

- The response should say the current metric is healthy if the value is `2`.
- It may mention that no recent log evidence was found.
- It should not invent a failure.

Q59. How do we test the endpoint during a known failure?

Replay a documented Phase 2 or Phase 3 OSPF failure, such as VLAN `440` loss,
then call:

```console
curl -s -X POST http://127.0.0.1:8080/explain-ospf \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "node": "R2",
    "protocol": "ospfv2",
    "lookback_minutes": 15
  }' | jq
```

Expected failure result:

- The response references the reduced neighbor count if Prometheus sees it.
- The response references adjacency logs if Loki has them.
- The response suggests verifying `enp0s1.440`, OVS trunks, FRR neighbors, and
  restoration state.

## 21. Run The Backend Manually

Q60. How do we start the backend for development?

```console
cd /path/to/network-security-lab/backend/phase5-ai
. .venv/bin/activate
uvicorn app.main:app --host 127.0.0.1 --port 8080 --reload
```

In a second terminal:

```console
curl -s http://127.0.0.1:8080/health | jq
```

Expected result:

- Uvicorn starts without import errors.
- `GET /health` returns JSON.
- FastAPI interactive docs are available locally at:

```text
http://127.0.0.1:8080/docs
```

Q61. How do we run it without reload?

```console
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

Use this mode before creating the systemd service.

## 22. Install The Backend As A systemd Service

Q62. Which service user should run the backend?

Use the normal lab user on the Management VM, for example `etu`. Adjust paths
if your user or repository location differs.

Q63. How do we create the systemd service?

On the Management VM:

```console
sudo tee /etc/systemd/system/phase5-ai-backend.service >/dev/null <<'EOF'
[Unit]
Description=Network Security Lab Phase 5 AI Backend
After=network-online.target prometheus.service loki.service
Wants=network-online.target

[Service]
Type=simple
User=etu
WorkingDirectory=/path/to/network-security-lab/backend/phase5-ai
EnvironmentFile=/path/to/network-security-lab/backend/phase5-ai/.env
ExecStart=/path/to/network-security-lab/backend/phase5-ai/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8080
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

Replace:

- `etu`
- `/path/to/network-security-lab`

Q64. How do we enable the service?

```console
sudo systemctl daemon-reload
sudo systemctl enable --now phase5-ai-backend
sudo systemctl status phase5-ai-backend --no-pager
journalctl -u phase5-ai-backend -n 80 --no-pager
```

Expected result:

- The service is active.
- No import error appears.
- No missing `API_TOKEN` error appears.

Q65. Should the backend listen on `0.0.0.0`?

For Phase 5, keep it on `127.0.0.1` unless another VM or frontend must call it.
If you expose it later:

- Bind only to the management network.
- Keep bearer-token authentication.
- Prefer a reverse proxy with access controls.
- Do not expose the backend publicly.

## 23. Validate The End To End AI Flow

Q66. What is the first complete test?

Use a known OSPF event:

```text
Lab event -> Prometheus/Loki evidence -> FastAPI -> Ollama on Mac -> AI answer
```

Q67. How do we run the complete test at baseline?

```console
cd /path/to/network-security-lab/backend/phase5-ai
export API_TOKEN="$(grep '^API_TOKEN=' .env | cut -d= -f2-)"

date -Ins
curl -s -X POST http://127.0.0.1:8080/explain-ospf \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"node":"R2","protocol":"ospfv2","lookback_minutes":30}' \
  | tee /tmp/phase5-ospf-explanation.json | jq -r '.answer'
date -Ins
```

Expected result:

- The backend answers through Ollama.
- The output mentions Prometheus and Loki evidence.
- The answer separates evidence from interpretation.

Q68. How do we run the complete test from a security incident?

If Phase 4 has a recent Suricata alert, copy the alert fields into:

```console
curl -s -X POST http://127.0.0.1:8080/explain-alert \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{
    "alert_name": "LOCAL Phase4 TCP SYN scan candidate",
    "labels": {
      "src_ip": "10.20.0.156",
      "dest_ip": "10.10.0.169",
      "node": "monitoring"
    },
    "annotations": {
      "summary": "Controlled Nmap scan detected inside the lab"
    }
  }' | jq -r '.answer'
```

Expected result:

- The answer identifies reconnaissance behavior.
- It says the scenario is controlled if that fact is supplied.
- It asks for PCAP, command output, and Suricata EVE JSON if missing.

Q69. What is the minimum accepted Phase 5 proof?

The proof is accepted when:

- `GET /health` reports Ollama, Prometheus, and Loki as reachable.
- `/chat` returns an answer through the Mac model.
- `/explain-log` explains a supplied FRR or Suricata log.
- `/explain-ospf` queries Prometheus and Loki.
- At least one answer says what evidence is missing instead of inventing it.

## 24. Add Observability For The Backend

Q70. How should backend logs reach Loki?

The backend runs under systemd on the Management VM. Phase 3 Alloy already
collects the systemd journal from the Management VM, so backend logs should
appear in Loki under:

```logql
{job="systemd-journal", node="management", unit="phase5-ai-backend.service"}
```

Q71. How do we generate a test log?

Restart the service and query logs:

```console
sudo systemctl restart phase5-ai-backend
journalctl -u phase5-ai-backend -n 50 --no-pager
```

In Grafana Explore:

```logql
{job="systemd-journal", node="management", unit="phase5-ai-backend.service"}
```

Expected result:

- Uvicorn startup logs appear locally.
- Loki receives the same service logs through Alloy.

Q72. Should the backend expose Prometheus metrics?

Not required in Phase 5. The first objective is a working AI bridge. If you add
metrics later, expose a `/metrics` endpoint and scrape it from Prometheus with
labels:

| Label | Value |
| --- | --- |
| `job` | `phase5-ai-backend` |
| `node` | `management` |
| `role` | `ai-backend` |

## 25. Save Evidence

Q73. What screenshots should be saved?

Save screenshots under `screenshots/phase5/`:

| Evidence | Suggested filename |
| --- | --- |
| Ollama model list | `phase5-ollama-model-list.png` |
| Ollama local API version | `phase5-ollama-local-version.png` |
| Management VM reaching Ollama | `phase5-management-ollama-connectivity.png` |
| FastAPI health endpoint | `phase5-fastapi-health.png` |
| FastAPI docs page | `phase5-fastapi-docs.png` |
| Chat endpoint response | `phase5-chat-response.png` |
| OSPF explanation response | `phase5-ospf-explanation.png` |
| Loki backend service logs | `phase5-loki-backend-logs.png` |

Q74. Which command outputs should be copied into the proof report?

Create `docs/proofs-phase5.md` and include:

```console
ollama --version
ollama list
ollama ps
```

```console
curl -s http://127.0.0.1:11434/api/version | jq
curl -s http://127.0.0.1:11434/api/tags | jq '.models[].name'
```

From the Management VM:

```console
curl -s "$MAC_OLLAMA_URL/api/version" | jq
curl -s http://127.0.0.1:8080/health | jq
systemctl status phase5-ai-backend --no-pager
```

Backend endpoint proof:

```console
curl -s -X POST http://127.0.0.1:8080/explain-ospf \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $API_TOKEN" \
  -d '{"node":"R2","protocol":"ospfv2","lookback_minutes":30}' | jq
```

Q75. Which files should be backed up?

| Node | Files |
| --- | --- |
| Mac | Ollama model list and benchmark output |
| Management VM | `backend/phase5-ai/app/main.py` |
| Management VM | `backend/phase5-ai/requirements.txt` |
| Management VM | `backend/phase5-ai/.env.example` |
| Management VM | `/etc/systemd/system/phase5-ai-backend.service` |
| Management VM | `docs/proofs-phase5.md` |

Do not commit `.env`, API tokens, SSH keys, Grafana cookies, or raw private
logs.

## 26. Troubleshooting

### Ollama Does Not Start

Q76. What should be checked on the Mac?

```console
ollama --version
ollama list
curl -s http://127.0.0.1:11434/api/version | jq
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

Common causes:

- Ollama application is not running.
- The CLI is installed but the service is not started.
- Another process is using port `11434`.
- The Mac needs an Ollama restart after environment changes.

### Model Pull Fails

Q77. What should be checked?

```console
df -h
ollama pull llama3.1:8b
ollama list
```

Common causes:

- Not enough disk space.
- Network interruption.
- Model tag typo.
- Proxy or certificate issue.

If the 14B models are too heavy, test with `llama3.1:8b` first and document
the resource limitation.

### Management VM Cannot Reach Ollama

Q78. What should be checked?

On the Mac:

```console
lsof -nP -iTCP:11434 -sTCP:LISTEN
```

On the Management VM:

```console
MAC_OLLAMA_URL="http://<mac-ip>:11434"
nc -vz <mac-ip> 11434
curl -v "$MAC_OLLAMA_URL/api/version"
```

Common causes:

- `OLLAMA_HOST` still binds only to `127.0.0.1`.
- Mac firewall blocks the Management VM.
- Wrong Mac IP address.
- VPN, Wi-Fi, or routing path changed.
- SSH tunnel is not running.

### FastAPI Fails To Start

Q79. What should be checked?

```console
cd /path/to/network-security-lab/backend/phase5-ai
. .venv/bin/activate
python -m pip check
uvicorn app.main:app --host 127.0.0.1 --port 8080
```

For systemd:

```console
sudo systemctl status phase5-ai-backend --no-pager
journalctl -u phase5-ai-backend -n 100 --no-pager
```

Common causes:

- Wrong `WorkingDirectory`.
- Wrong `.venv` path.
- Missing `.env`.
- Missing `API_TOKEN`.
- Python dependency installation failed.

### Backend Returns 401

Q80. What should be checked?

```console
grep '^API_TOKEN=' .env
echo "$API_TOKEN"
```

Then retry with:

```console
-H "Authorization: Bearer $API_TOKEN"
```

Do not paste the real token into public documentation.

### Backend Cannot Query Prometheus Or Loki

Q81. What should be checked on the Management VM?

```console
curl -s http://127.0.0.1:9090/-/ready
curl -s http://127.0.0.1:3100/ready
curl -s "http://127.0.0.1:9090/api/v1/query" --data-urlencode 'query=up' | jq
curl -G -s "http://127.0.0.1:3100/loki/api/v1/labels" | jq
```

Common causes:

- Prometheus or Loki is down.
- The backend `.env` points to the wrong URL.
- Loki has no logs in the selected time range.
- Prometheus metric names changed.

### AI Answer Hallucinates

Q82. What should be changed?

Improve the prompt and supplied evidence:

- Add exact timestamps.
- Add raw metric values.
- Add raw log excerpts.
- Ask for a `Missing data` section.
- Ask for verification commands.
- Lower temperature.
- Use the code model for configuration-heavy questions.

Do not hide hallucinations in the proof report. Document them as limitations
and adjust the prompt.

## 27. Conclusion

This Phase 5 lab connects the network security platform to local AI inference
without moving the project away from its core evidence.

The exit criteria are satisfied when:

- Ollama runs on the MacBook Pro.
- The planned models are pulled and benchmarked.
- The Management VM can reach the Ollama API through a controlled path.
- FastAPI runs on the Management VM.
- The backend has protected endpoints for chat, summary, logs, alerts, and OSPF
  explanation.
- The backend can query Prometheus and Loki.
- At least one OSPF or IDS event is explained from supplied evidence.
- The answer clearly states missing data when evidence is incomplete.

Phase 6 can now build on this foundation by improving prompts, adding incident
workflows, evaluating response quality, and preparing the assistant for RAG.

## 28. References

- InetDoc OSPF practical lab style and structure: <https://inetdoc.net/travaux_pratiques/interco_05.ospf/>
- Ollama API introduction: <https://docs.ollama.com/api/introduction>
- Ollama FAQ and server environment variables: <https://docs.ollama.com/faq>
- Ollama embedding API: <https://docs.ollama.com/api/embed>
- Ollama `qwen2.5` model library: <https://ollama.com/library/qwen2.5>
- Ollama `llama3.1` model library: <https://ollama.com/library/llama3.1>
- Ollama `qwen2.5-coder` model library: <https://ollama.com/library/qwen2.5-coder>
- Ollama `nomic-embed-text` model library: <https://ollama.com/library/nomic-embed-text>
- FastAPI first steps: <https://fastapi.tiangolo.com/tutorial/first-steps/>
- FastAPI settings and environment variables: <https://fastapi.tiangolo.com/advanced/settings/>
- FastAPI deployment concepts: <https://fastapi.tiangolo.com/deployment/concepts/>
- Uvicorn deployment notes: <https://uvicorn.dev/deployment/>
