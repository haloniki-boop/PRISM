# ./src/api/routers/classify.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from ..core.config import AppSettings, get_settings
from ..core.llm_client import LLMClient
from ..core.mcp_client import MCPClient
from ..core.plugins import PluginRegistry, classify_item, load_plugins

router = APIRouter()


class Item(BaseModel):
    title: str = ""
    body: str = ""
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class ClassifyRequest(BaseModel):
    items: List[Item]


class ClassifyResponse(BaseModel):
    results: List[Dict[str, Any]]


def require_api_key(x_api_key: Optional[str] = Header(default=None), settings: AppSettings = Depends(get_settings)) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}})


@router.post("/classify", response_model=ClassifyResponse)
async def classify_endpoint(payload: ClassifyRequest, _auth: None = Depends(require_api_key), settings: AppSettings = Depends(get_settings)):
    registry: PluginRegistry = load_plugins(settings)
    llm = LLMClient(settings)
    notion = MCPClient(settings)

    results: List[Dict[str, Any]] = []
    for item in payload.items:
        result = await classify_item(item.model_dump(), registry=registry, llm=llm, notion=notion, config=settings)
        results.append(result)
    return {"results": results}

# EOF ./src/api/routers/classify.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成