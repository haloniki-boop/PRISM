# ./tests/test_plugins.py - v1.0.0
from __future__ import annotations

from src.api.core.config import get_settings
from src.api.core.plugins import PluginRegistry, load_plugins


def test_plugins_load():
    settings = get_settings()
    registry = load_plugins(settings)
    names = [p.name for p in registry.all()]
    assert "task_classifier" in names
    assert "knowledge_classifier" in names
    assert "note_classifier" in names
    assert "template" in names

# EOF ./tests/test_plugins.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成