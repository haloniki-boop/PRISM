# ./src/api/plugins/task_classifier.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict


def register() -> dict:
    return {
        "name": "task_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["task"],
    }


def classify(item: Dict[str, Any], *, llm, notion, config) -> Dict[str, Any]:
    title = (item.get("title") or "").lower()
    body = (item.get("body") or "").lower()
    text = f"{title} {body}"

    hints = ["todo", "due", "deadline", "asap", "fix", "implement", "対応", "する"]
    if any(k in text for k in hints):
        return {"type": "Task", "score": 0.9, "tags": ["task"], "reason": "task keywords"}
    return {"type": "Note", "score": 0.3, "tags": [], "reason": "no strong task signal"}

# EOF ./src/api/plugins/task_classifier.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成