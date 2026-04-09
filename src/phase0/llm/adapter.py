from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from typing import Any

from src.phase0.core.config import settings


class LLMConnectionError(Exception):
    pass


class LLMClientAdapter:
    def __init__(self, *, timeout_seconds: int = 45, max_retries: int = 2) -> None:
        self.timeout_seconds = timeout_seconds
        self.max_retries = max_retries
        self.api_url = "https://api.groq.com/openai/v1/chat/completions"

    def generate(self, prompt: str, *, metadata: dict[str, Any] | None = None) -> str:
        if not settings.groq_api_key:
            raise LLMConnectionError("GROQ_API_KEY is not configured.")

        system_msg = (
            "You are a restaurant recommendation ranker. "
            "Return strict JSON only. Do not include markdown. "
            "Generate unique, personalized descriptions for each restaurant based on its specific characteristics. "
            "Never use generic or repetitive explanations - each restaurant description must be different and highlight what makes it special."
        )
        payload = {
            "model": settings.groq_model,
            "messages": [
                {"role": "system", "content": system_msg},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.7,
            "max_tokens": 900,
            "response_format": {"type": "json_object"},
        }
        body = json.dumps(payload).encode("utf-8")
        headers = {
            "Authorization": f"Bearer {settings.groq_api_key}",
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        }

        last_error: Exception | None = None
        for attempt in range(self.max_retries + 1):
            try:
                request = urllib.request.Request(
                    self.api_url,
                    data=body,
                    headers=headers,
                    method="POST",
                )
                with urllib.request.urlopen(request, timeout=self.timeout_seconds) as response:
                    raw = response.read().decode("utf-8")
                parsed = json.loads(raw)
                content = parsed["choices"][0]["message"]["content"]
                if not isinstance(content, str) or not content.strip():
                    raise LLMConnectionError("Groq response content was empty.")
                return content
            except (urllib.error.HTTPError, urllib.error.URLError, KeyError, json.JSONDecodeError) as exc:
                last_error = exc
                if attempt >= self.max_retries:
                    break
                time.sleep(2**attempt)

        raise LLMConnectionError(f"Groq request failed after retries: {last_error}")
