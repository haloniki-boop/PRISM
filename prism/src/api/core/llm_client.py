# ./src/api/core/llm_client.py - v1.0.0
from __future__ import annotations

import os
from typing import Optional

import httpx

from .config import AppSettings


class LLMClient:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def complete(self, prompt: str, system: Optional[str] = None, temperature: Optional[float] = None) -> str:
        # In mock mode, return heuristic output
        if self.settings.runtime.mock_mode or not self.settings.llm.api_key:
            # Simple heuristic for classification-like prompts
            text = prompt.lower()
            if "todo" in text or "deadline" in text or "due" in text or "する" in text:
                return "Task"
            if "how to" in text or "手順" in text or "仕様" in text or "reference" in text:
                return "Knowledge"
            return "Note"

        # Minimal OpenAI Chat Completions HTTP call (no SDK dep)
        temperature = temperature if temperature is not None else self.settings.llm.temperature
        headers = {
            "Authorization": f"Bearer {self.settings.llm.api_key}",
            "Content-Type": "application/json",
        }
        payload = {
            "model": self.settings.llm.model,
            "messages": ([{"role": "system", "content": system}] if system else []) + [{"role": "user", "content": prompt}],
            "temperature": temperature,
        }
        async with httpx.AsyncClient(timeout=30.0) as client:
            resp = await client.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            return data["choices"][0]["message"]["content"].strip()


__all__ = ["LLMClient"]

# EOF ./src/api/core/llm_client.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成