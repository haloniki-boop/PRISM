#!/bin/bash
API_URL="http://localhost:8060"
API_KEY="changeme-api-key"

echo "デバッグテスト: 今日の気づき"
curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{"items":[{"title":"今日の気づき","body":"プロジェクトでの学び"}]}' | jq '.'
