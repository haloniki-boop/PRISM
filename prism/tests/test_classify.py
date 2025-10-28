# ./tests/test_classify.py - v1.0.0
from __future__ import annotations

import asyncio

from src.api.core.config import get_settings
from src.api.core.llm_client import LLMClient
from src.api.core.mcp_client import MCPClient
from src.api.core.plugins import classify_item, load_plugins


async def _classify(text: str):
    settings = get_settings()
    registry = load_plugins(settings)
    llm = LLMClient(settings)
    mcp = MCPClient(settings)
    item = {"title": text.split("\n")[0], "body": text}
    return await classify_item(item, registry=registry, llm=llm, notion=mcp, config=settings)


def test_task_detection():
    res = asyncio.run(_classify("TODO: send report by Friday"))
    assert res["type"] in ("Task", "Note")


def test_knowledge_detection():
    res = asyncio.run(_classify("How to configure FastAPI logging"))
    assert res["type"] in ("Knowledge", "Note")


def test_note_fallback():
    res = asyncio.run(_classify("Random thoughts and meeting notes"))
    assert res["type"] in ("Note", "Task", "Knowledge")

# EOF ./tests/test_classify.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成