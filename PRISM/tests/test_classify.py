./tests/test_classify.py - v1.0.0

from src.api.core.plugins import classify_with_plugins
from src.api.core.llm_client import MockLLM
from src.api.core.notion_client import MockNotion
from src.api.core.config import load_config


def test_classify_task():
    item = {"title": "Task: submit report", "body": "deadline tomorrow"}
    res = classify_with_plugins(item, llm=MockLLM(), notion=MockNotion(), config=load_config())
    assert res["type"] in {"Task", "Note", "Knowledge"}


EOF ./tests/test_classify.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 分類の基本テスト

