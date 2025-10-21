./tests/test_plugins.py - v1.0.0

from src.api.core.plugins import discover_plugins


def test_discover_plugins():
    plugins = discover_plugins()
    assert "template" in plugins
    assert any(p.labels for p in plugins.values())

EOF ./tests/test_plugins.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: プラグインローダの基本テスト

