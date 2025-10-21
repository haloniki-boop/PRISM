
from typing import List


def register() -> dict:
    return {
        "name": "task_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["task"],
    }


def classify(item: dict, *, llm, notion, config) -> dict:
    text = f"{item.get('title', '')}\n{item.get('body', '')}".lower()
    
    # Task特有のキーワード（日本語・英語）
    task_indicators = [
        "todo", "task", "deadline", "due", "schedule", "assign",
        "タスク", "締切", "期限", "予定", "やること", "実施",
        "完了", "実行", "作業", "提出", "レポート", "準備"
    ]
    
    has_task_keyword = any(k in text for k in task_indicators)
    
    if has_task_keyword:
        score = 0.9
        category = "Task"
        reason = "keyword match"
        tags = list(set([*item.get("tags", []), "task"]))
    else:
        # タスクキーワードが無い場合は低スコアを返す
        score = 0.2
        category = "Task"
        reason = "no task keyword"
        tags = item.get("tags", [])
    
    return {"type": category, "score": score, "tags": tags, "reason": reason}


