# ./src/api/routers/sync.py - v1.0.0
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException

from ..core.config import AppSettings, get_settings
from ..core.llm_client import LLMClient
from ..core.mcp_client import MCPClient
from ..core.plugins import classify_item, load_plugins
from .query import add_to_store

router = APIRouter()


def require_api_key(x_api_key: Optional[str] = Header(default=None), settings: AppSettings = Depends(get_settings)) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}})


@router.post("/sync/notion")
async def sync_notion(_auth: None = Depends(require_api_key), settings: AppSettings = Depends(get_settings)):
    registry = load_plugins(settings)
    llm = LLMClient(settings)
    mcp = MCPClient(settings)

    pages = await mcp.fetch_pages(limit=10)
    count = 0
    for p in pages:
        result = await classify_item(p, registry=registry, llm=llm, notion=mcp, config=settings)
        add_to_store({**p, **result})
        count += 1
    return {"synced": count}

# EOF ./src/api/routers/sync.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成