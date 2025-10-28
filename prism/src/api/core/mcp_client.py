# ./src/api/core/mcp_client.py - v1.0.0
from __future__ import annotations

import random
import time
from typing import Any, Dict, List, Optional

from .config import AppSettings


class MCPClient:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def fetch_pages(self, limit: int = 10) -> List[Dict[str, Any]]:
        if self.settings.runtime.mock_mode:
            return _mock_pages(limit)
        # Real MCP integration would go here (HTTP/RPC)
        raise NotImplementedError("MCP live mode not implemented in this demo")

    async def fetch_page(self, page_id: str) -> Dict[str, Any]:
        if self.settings.runtime.mock_mode:
            return _mock_page(page_id)
        raise NotImplementedError

    async def update_tags(self, page_id: str, tags: List[str]) -> bool:
        if self.settings.runtime.mock_mode:
            return True
        raise NotImplementedError


# --- Mock helpers ---
MOCK_SAMPLE_BODIES = [
    "Buy milk and send invoice by Friday.",
    "How to configure FastAPI logging for production.",
    "Meeting notes from weekly sync with team.",
    "Implement backup routine and verify retention policy.",
    "API reference for internal microservice endpoints.",
    "Idea dump: new onboarding flow thoughts.",
]


def _mock_pages(limit: int) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for i in range(limit):
        pid = f"mock-{int(time.time())}-{i}"
        out.append(_mock_page(pid))
    return out


def _mock_page(page_id: str) -> Dict[str, Any]:
    body = random.choice(MOCK_SAMPLE_BODIES)
    return {
        "id": page_id,
        "title": body.split(".")[0][:40],
        "body": body,
        "properties": {"created": "2025-10-20"},
        "tags": ["mock"],
    }


__all__ = ["MCPClient"]

# EOF ./src/api/core/mcp_client.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成