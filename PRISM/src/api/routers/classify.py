
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel, Field

from ..core.config import load_config
from ..core.plugins import classify_with_plugins
from ..core import llm_client, notion_client


router = APIRouter(prefix="", tags=["classify"])


class ItemModel(BaseModel):
    title: str
    body: Optional[str] = None
    properties: Dict[str, Any] = Field(default_factory=dict)
    tags: List[str] = Field(default_factory=list)


class BatchRequest(BaseModel):
    items: List[ItemModel]


def get_clients():
    cfg = load_config()
    llm = llm_client.MockLLM()
    notion = notion_client.MockNotion()
    return cfg, llm, notion


def require_api_key(x_api_key: Optional[str] = Header(default=None)):
    cfg = load_config()
    expected = cfg.api_key
    if expected and x_api_key != expected:
        raise HTTPException(status_code=401, detail={"error": {"code": "unauthorized", "message": "Invalid API key"}})


@router.post("/classify")
def classify_endpoint(payload: BatchRequest, _=Depends(require_api_key)):
    cfg, llm, notion = get_clients()
    results = []
    for item in payload.items:
        result = classify_with_plugins(item.model_dump(), llm=llm, notion=notion, config=cfg)
        results.append(result)
    return {"results": results}


@router.post("/sync/notion")
def sync_notion(_=Depends(require_api_key)):
    # Mock sync for now
    return {"status": "queued"}

