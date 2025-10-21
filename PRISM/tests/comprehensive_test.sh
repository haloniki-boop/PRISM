#!/bin/bash
API_URL="http://localhost:8060"
API_KEY="changeme-api-key"

echo "================================"
echo "PRISM 包括的テスト - v1.1.0"
echo "================================"
echo ""

total=0
passed=0
failed=0

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
    
    echo "   スコア: $result_score | 理由: $result_reason"
}

# === タスクケース ===
echo "【タスク分類テスト】"
run_test "タスク1" "レポート提出" "明日までにレポートを提出する" "Task"
run_test "タスク2" "Todo: ミーティング準備" "来週のスケジュールを準備" "Task"
run_test "タスク3" "期限管理" "プロジェクトの締切は金曜日" "Task"
run_test "タスク4" "作業リスト" "実施する予定のタスク一覧" "Task"
echo ""

# === 知識ケース ===
echo "【知識分類テスト】"
run_test "知識1" "Dockerの使い方" "コンテナ技術の基本とdocker-composeの手順" "Knowledge"
run_test "知識2" "システム設計" "アーキテクチャ設計のリファレンスドキュメント" "Knowledge"
run_test "知識3" "API開発ガイド" "RESTful APIの設計原理と実装方法" "Knowledge"
run_test "知識4" "技術解説" "プログラミング言語の仕組みについて" "Knowledge"
echo ""

# === ノートケース ===
echo "【ノート分類テスト】"
run_test "ノート1" "今日の気づき" "プロジェクトでの学びと気づき" "Note"
run_test "ノート2" "会議メモ" "本日の会議内容を記録しました" "Note"
run_test "ノート3" "日記" "今日の出来事と感想" "Note"
run_test "ノート4" "備忘録" "忘れないように覚書として記録" "Note"
run_test "ノート5" "思考メモ" "考えたことを整理して記録" "Note"
run_test "ノート6" "観察記録" "プロジェクトの振り返りと観察" "Note"
echo ""

# === エッジケース ===
echo "【エッジケース】"
run_test "エッジ1" "空のタイトル" "" "Note"
run_test "エッジ2" "短いテキスト" "メモ" "Note"
run_test "エッジ3" "複合キーワード" "会議メモ タスク管理について" "Note"
run_test "エッジ4" "英語のみ" "Meeting notes for project review" "Note"
echo ""

# === 複数アイテム同時テスト ===
echo "【複数アイテム同時分類】"
response=$(curl -s -X POST "$API_URL/classify" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $API_KEY" \
  -d '{
    "items": [
      {"title":"Todo: ミーティング準備","body":"schedule for next week"},
      {"title":"システム設計","body":"architecture reference document"},
      {"title":"日記","body":"今日の記録"}
    ]
  }')

echo "複数アイテムテスト結果:"
echo "$response" | jq -r '.results[] | "  - \(.type) (スコア: \(.score))"'
echo ""

echo "================================"
echo "テスト結果サマリー"
echo "================================"
echo "総テスト数: $total"
echo "✅ 合格: $passed ($((passed * 100 / total))%)"
echo "❌ 不合格: $failed ($((failed * 100 / total))%)"
echo ""

if [ $failed -eq 0 ]; then
    echo "🎉 全テスト合格！分類エンジンは正常に動作しています。"
    exit 0
else
    echo "⚠️ 一部テスト失敗 - 要確認"
    exit 1
fi
