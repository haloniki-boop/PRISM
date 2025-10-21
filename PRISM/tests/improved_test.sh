#!/bin/bash
API_URL="http://localhost:8060"
API_KEY="changeme-api-key"

echo "================================"
echo "PRISM 改修後テスト - v1.1.0"
echo "================================"
echo ""

total=0
passed=0
failed=0

# テスト関数
run_test() {
    local name=$1
    local title=$2
    local body=$3
    local expected=$4
    
    total=$((total + 1))
    
    echo "----------------------------"
    echo "テスト #$total: $name"
    echo "入力: $title"
    
    response=$(curl -s -X POST "$API_URL/classify" \
        -H "Content-Type: application/json" \
        -H "X-API-Key: $API_KEY" \
        -d "{\"items\":[{\"title\":\"$title\",\"body\":\"$body\"}]}")
    
    result_type=$(echo "$response" | jq -r '.results[0].type')
    result_score=$(echo "$response" | jq -r '.results[0].score')
    result_reason=$(echo "$response" | jq -r '.results[0].reason')
    
    if [ "$result_type" == "$expected" ]; then
        echo "✅ 合格: $result_type (期待: $expected)"
        passed=$((passed + 1))
    else
        echo "❌ 不合格: $result_type (期待: $expected)"
        failed=$((failed + 1))
    fi
    
    echo "   スコア: $result_score"
    echo "   理由: $result_reason"
    echo ""
}

# タスク分類テスト
run_test "タスク1" "レポート提出" "明日までにレポートを提出。deadline tomorrow" "Task"
run_test "タスク2" "Todo: ミーティング準備" "schedule for next week" "Task"

# 知識分類テスト
run_test "知識1" "Dockerの使い方" "コンテナ技術の基本。how to use containers" "Knowledge"
run_test "知識2" "システム設計" "architecture reference document" "Knowledge"

# ノート分類テスト（改善対象）
run_test "ノート1" "今日の気づき" "プロジェクトでの学び" "Note"
run_test "ノート2" "会議メモ" "本日の会議内容を記録" "Note"
run_test "ノート3" "日記" "今日の出来事" "Note"
run_test "ノート4" "備忘録" "覚えておくべきこと" "Note"

# エッジケース
run_test "エッジ1" "思考メモ" "考えたことを記録" "Note"
run_test "エッジ2" "単純メモ" "何かのメモ" "Note"

echo "================================"
echo "テスト結果サマリー"
echo "================================"
echo "総テスト数: $total"
echo "✅ 合格: $passed ($((passed * 100 / total))%)"
echo "❌ 不合格: $failed ($((failed * 100 / total))%)"
echo ""

if [ $failed -eq 0 ]; then
    echo "🎉 全テスト合格！"
    exit 0
else
    echo "⚠️ 一部テスト失敗 - 要確認"
    exit 1
fi
