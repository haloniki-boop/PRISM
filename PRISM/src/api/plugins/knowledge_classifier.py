
from typing import List


def register() -> dict:
    return {
        "name": "knowledge_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["knowledge"],
    }


def classify(item: dict, *, llm, notion, config) -> dict:
    text = f"{item.get('title', '')}\n{item.get('body', '')}".lower()
    
    # Knowledge特有のキーワード（日本語・英語）
    knowledge_indicators = [
        "how to", "architecture", "design", "reference", "knowledge", "faq",
        "設計", "アーキテクチャ", "ナレッジ", "知識", "技術", "方法",
        "使い方", "手順", "仕組み", "原理", "解説", "ドキュメント",
        "システム", "docker", "api", "プログラミング", "開発"
    ]
    
    has_knowledge_keyword = any(k in text for k in knowledge_indicators)
    
    if has_knowledge_keyword:
        score = 0.85
        category = "Knowledge"
        reason = "keyword match"
        tags = list(set([*item.get("tags", []), "knowledge"]))
    else:
        # Knowledgeキーワードが無い場合は低スコアを返す
        score = 0.2
        category = "Knowledge"
        reason = "no knowledge keyword"
        tags = item.get("tags", [])
    
    return {"type": category, "score": score, "tags": tags, "reason": reason}


