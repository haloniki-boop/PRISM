# ./src/api/core/notion_client.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict, List

from .config import AppSettings


class NotionClient:
    def __init__(self, settings: AppSettings):
        self.settings = settings

    async def fetch_pages(self, limit: int = 10) -> List[Dict[str, Any]]:
        # For this demo, Notion client mirrors MCP interface; real API omitted
        raise NotImplementedError("Notion client is not implemented; use MCP mock in tests")

    async def fetch_page(self, page_id: str) -> Dict[str, Any]:
        raise NotImplementedError

    async def update_tags(self, page_id: str, tags: List[str]) -> bool:
        raise NotImplementedError


__all__ = ["NotionClient"]

# EOF ./src/api/core/notion_client.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成