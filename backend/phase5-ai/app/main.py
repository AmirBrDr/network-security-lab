from __future__ import annotations

import secrets
import time
from functools import lru_cache
from typing import Any, Literal

import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, status
from pydantic import BaseModel, Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    app_name: str = "network-security-lab-ai"
    api_token: str
    ollama_url: str = "http://127.0.0.1:11434"
    default_model: str = "qwen2.5-coder:7b-instruct"
    fast_model: str = "llama3.2:3b"
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
    if authorization is None or not secrets.compare_digest(authorization, expected):
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
    node: str = Field(default="R2", max_length=40, pattern=r"^[A-Za-z0-9_.-]+$")
    protocol: Literal["ospfv2", "ospfv3"] = "ospfv2"
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
