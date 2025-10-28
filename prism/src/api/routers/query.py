# ./src/api/routers/query.py - v1.0.0
from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException, Query

from ..core.config import AppSettings, get_settings

router = APIRouter()


# Very simple in-memory store for demo purposes
_STORE: List[Dict[str, Any]] = []


def add_to_store(item: Dict[str, Any]) -> None:
    _STORE.append(item)


def require_api_key(x_api_key: Optional[str] = Header(default=None), settings: AppSettings = Depends(get_settings)) -> None:
    if not x_api_key or x_api_key != settings.api_key:
        raise HTTPException(status_code=401, detail={"error": {"code": "UNAUTHORIZED", "message": "Invalid API key"}})


@router.get("/query")
async def query_items(
    _auth: None = Depends(require_api_key),
    type: Optional[str] = Query(default=None),
    tag: Optional[str] = Query(default=None),
    start: Optional[str] = Query(default=None),
    end: Optional[str] = Query(default=None),
):
    def in_range(dt: str) -> bool:
        if not start and not end:
            return True
        try:
            d = datetime.fromisoformat(dt)
            if start and d < datetime.fromisoformat(start):
                return False
            if end and d > datetime.fromisoformat(end):
                return False
            return True
        except Exception:
            return True

    results = []
    for it in _STORE:
        if type and it.get("type") != type:
            continue
        if tag and tag not in it.get("tags", []):
            continue
        created = (it.get("properties", {}) or {}).get("created", "")
        if created and not in_range(created):
            continue
        results.append(it)
    return {"results": results}

# EOF ./src/api/routers/query.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成