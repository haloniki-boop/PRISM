# ./src/api/plugins/knowledge_classifier.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict


def register() -> dict:
    return {
        "name": "knowledge_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["knowledge"],
    }


def classify(item: Dict[str, Any], *, llm, notion, config) -> Dict[str, Any]:
    title = (item.get("title") or "").lower()
    body = (item.get("body") or "").lower()
    text = f"{title} {body}"

    hints = ["how to", "手順", "reference", "api", "spec", "仕様", "design"]
    if any(k in text for k in hints):
        return {"type": "Knowledge", "score": 0.85, "tags": ["knowledge"], "reason": "knowledge keywords"}
    return {"type": "Note", "score": 0.4, "tags": [], "reason": "no strong knowledge signal"}

# EOF ./src/api/plugins/knowledge_classifier.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成