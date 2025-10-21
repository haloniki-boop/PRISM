
from typing import List


def register() -> dict:
    return {
        "name": "note_classifier",
        "version": "v1.1.0",
        "capabilities": ["classify"],
        "labels": ["note"],
    }


def classify(item: dict, *, llm, notion, config) -> dict:
    text = f"{item.get('title', '')}\n{item.get('body', '')}".lower()
    
    # Note特有のキーワード（日本語・英語）
    note_indicators = [
        "メモ", "気づき", "記録", "日記", "備忘", "覚書",
        "memo", "note", "diary", "observation", "記憶", "思考",
        "会議メモ", "meeting notes", "学び", "learning",
        "振り返り", "reflection", "感想", "impression"
    ]
    
    # タスクやナレッジの強いキーワードがないかチェック
    task_keywords = ["todo", "task", "deadline", "due", "schedule", "assign"]
    knowledge_keywords = ["how to", "architecture", "design", "reference", "knowledge", "faq"]
    
    has_task = any(k in text for k in task_keywords)
    has_knowledge = any(k in text for k in knowledge_keywords)
    has_note = any(k in text for k in note_indicators)
    
    # スコアリングロジック
    if has_note and not has_task and not has_knowledge:
        # Note特有のキーワードがあり、他のカテゴリのキーワードがない
        score = 0.8
        category = "Note"
        reason = "note keyword match"
    elif not has_task and not has_knowledge and not has_note:
        # どのキーワードもない場合はNoteにフォールバック
        score = 0.6
        category = "Note"
        reason = "fallback to note"
    else:
        # 他のカテゴリのキーワードがある場合は低スコア
        score = 0.3
        category = "Note"
        reason = "low confidence"
    
    tags: List[str] = list(set([*item.get("tags", []), "note"])) if category == "Note" else item.get("tags", [])
    return {"type": category, "score": score, "tags": tags, "reason": reason}


