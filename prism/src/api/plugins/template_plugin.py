# ./src/api/plugins/template_plugin.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict, List


def register() -> dict:
    return {
        "name": "template",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["task", "knowledge", "note"],
    }


def classify(item: Dict[str, Any], *, llm, notion, config) -> Dict[str, Any]:
    title = (item.get("title") or "").lower()
    body = (item.get("body") or "").lower()
    text = f"{title}\n{body}"

    # Heuristic + LLM fallback
    if any(k in text for k in ["deadline", "due", "todo", "する", "対応", "fix", "implement"]):
        return {"type": "Task", "score": 0.8, "tags": ["auto"], "reason": "keyword heuristic"}
    if any(k in text for k in ["how to", "手順", "reference", "spec", "仕様", "design"]):
        return {"type": "Knowledge", "score": 0.7, "tags": ["auto"], "reason": "keyword heuristic"}

    # LLM mock returns type string; map to default score
    predicted = ""  # default
    try:
        predicted = getattr(llm, "complete")("Classify as Task/Knowledge/Note: " + text)
        if hasattr(predicted, "__await__"):
            predicted = None  # will be awaited by caller if needed
    except Exception:
        predicted = "Note"

    if isinstance(predicted, str):
        label = predicted.strip()
        score = 0.6 if label in ("Task", "Knowledge") else 0.5
        return {"type": label if label in ("Task", "Knowledge", "Note") else "Note", "score": score, "tags": ["llm"], "reason": "llm"}

    # If async path, assume caller awaits classify result via plugins.classify_item wrapper
    return {"type": "Note", "score": 0.5, "tags": ["default"], "reason": "fallback"}

# EOF ./src/api/plugins/template_plugin.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成