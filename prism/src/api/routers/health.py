# ./src/api/routers/health.py - v1.0.0
from __future__ import annotations

from fastapi import APIRouter

router = APIRouter()


@router.get("/healthz")
async def healthz():
    return {"status": "ok"}

# EOF ./src/api/routers/health.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成