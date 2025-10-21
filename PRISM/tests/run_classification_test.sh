#!/bin/bash

# PRISM 分類テストスクリプト
# 使用方法: ./run_classification_test.sh

API_URL="http://localhost:8060"
API_KEY="changeme-api-key"
TEST_DATA="test_data.json"

echo "================================"
echo "PRISM 分類機能テスト開始"
echo "================================"
echo ""

# テストデータを読み込み
if [ ! -f "$TEST_DATA" ]; then
    echo "エラー: $TEST_DATA が見つかりません"
    exit 1
fi

# カウンター初期化
total=0
passed=0
failed=0

# JSONから各テストケースを抽出して実行
cat "$TEST_DATA" | jq -c '.test_cases[]' | while read -r test_case; do
    name=$(echo "$test_case" | jq -r '.name')
    title=$(echo "$test_case" | jq -r '.input.title')
    body=$(echo "$test_case" | jq -r '.input.body')
    tags=$(echo "$test_case" | jq -c '.input.tags')
    expected=$(echo "$test_case" | jq -r '.expected_type')
    
    total=$((total + 1))
    
    echo "----------------------------"
    echo "テスト #$total: $name"
    echo "入力: $title"
    
    # API リクエスト作成
    request_body=$(jq -n \
        --arg title "$title" \
        --arg body "$body" \
        --argjson tags "$tags" \
        '{items: [{title: $title, body: $body, tags: $tags}]}')
    
    # API 呼び出し
    response=$(curl -s -X POST "$API_URL/classify" \
        -H "Content-Type: application/json" \
        -H "X-API-Key: $API_KEY" \
        -d "$request_body")
    
    # 結果を解析
    result_type=$(echo "$response" | jq -r '.results[0].type')
    result_score=$(echo "$response" | jq -r '.results[0].score')
    result_tags=$(echo "$response" | jq -c '.results[0].tags')
    result_reason=$(echo "$response" | jq -r '.results[0].reason')
    
    # 判定
    if [ "$result_type" == "$expected" ]; then
        echo "✅ 合格: $result_type (期待: $expected)"
        passed=$((passed + 1))
    else
        echo "❌ 不合格: $result_type (期待: $expected)"
        failed=$((failed + 1))
    fi
    
    echo "   スコア: $result_score"
    echo "   タグ: $result_tags"
    echo "   理由: $result_reason"
    echo ""
done

# 最終結果
echo "================================"
echo "テスト結果サマリー"
echo "================================"
echo "合格: $passed / $total"
echo "不合格: $failed / $total"
if [ $failed -eq 0 ]; then
    echo "✅ 全テスト合格！"
else
    echo "⚠️  一部テスト失敗"
fi
echo ""

