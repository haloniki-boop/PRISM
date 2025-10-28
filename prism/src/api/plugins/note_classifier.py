# ./src/api/plugins/note_classifier.py - v1.0.0
from __future__ import annotations

from typing import Any, Dict


def register() -> dict:
    return {
        "name": "note_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["note"],
    }


def classify(item: Dict[str, Any], *, llm, notion, config) -> Dict[str, Any]:
    # Default fallback to Note with mild score
    return {"type": "Note", "score": 0.6, "tags": ["note"], "reason": "default note bias"}

# EOF ./src/api/plugins/note_classifier.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成