#!/bin/bash
API_URL="http://localhost:8060"
API_KEY="changeme-api-key"

echo "================================"
echo "PRISM 分類機能テスト"
echo "================================"
echo ""

# テスト1: タスク
echo "テスト1: タスク分類"
curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"items":[{"title":"レポート提出","body":"明日までにレポートを提出。deadline tomorrow"}]}' | jq '.'
echo ""

# テスト2: 知識
echo "テスト2: 知識分類"
curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"items":[{"title":"Dockerの使い方","body":"コンテナ技術の基本。how to use containers"}]}' | jq '.'
echo ""

# テスト3: ノート
echo "テスト3: ノート分類"
curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"items":[{"title":"今日の気づき","body":"プロジェクトでの学び"}]}' | jq '.'
echo ""

# テスト4: 複数アイテム同時
echo "テスト4: 複数アイテム同時分類"
curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "items": [
      {"title":"Todo: ミーティング準備","body":"schedule for next week"},
      {"title":"システム設計","body":"architecture reference document"},
      {"title":"メモ","body":"今日の記録"}
    ]
  }' | jq '.'
echo ""

echo "================================"
echo "テスト完了"
echo "================================"
