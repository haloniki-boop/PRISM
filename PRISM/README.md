./README.md - v1.0.0

# PRISM - 分類・問い合わせ可能なToDo/習慣/知識ベース

Notionに入力されたデータをChatGPTで「Task／知識／Note」に自動分類・仕訳し、自然言語で問い合わせ可能なToDo／習慣／知識ベースへ整理するシステム。

## 🚀 クイックスタート

### 1. 前提条件
- Docker & Docker Compose がインストール済み
- Git がインストール済み

### 2. セットアップ手順

```bash
# リポジトリをクローン
git clone <repository-url>
cd PRISM

# 環境変数ファイルを作成
cp env.example .env

# .env ファイルを編集（必要に応じて）
# API_KEY, OPENAI_API_KEY, NOTION_API_KEY を設定

# サービス起動
docker-compose up -d

# 起動確認
docker-compose ps
```

### 3. アクセス先

- **Web UI**: http://localhost:8061
- **API**: http://localhost:8060
- **ヘルスチェック**: http://localhost:8060/healthz

## 📋 機能

### 分類機能
- Notionページを「Task」「Knowledge」「Note」に自動分類
- キーワードベースの分類ロジック
- プラグイン方式で拡張可能

### 検索機能
- 自然言語での検索
- タイプ別フィルタ（Task/Knowledge/Note）
- タグ別フィルタ
- 日付範囲フィルタ

### API エンドポイント

#### 分類
```bash
POST /classify
Content-Type: application/json
X-API-Key: prism-dev-key-2025

{
  "items": [
    {
      "title": "Task: submit report",
      "body": "deadline tomorrow",
      "tags": []
    }
  ]
}
```

#### 検索
```bash
GET /query?q=report&type=Task&tag=urgent
```

#### ヘルスチェック
```bash
GET /healthz
```

## 🔧 設定

### 環境変数 (.env)

```bash
# 基本設定
PRISM_ENV=development
API_KEY=prism-dev-key-2025

# 外部サービス連携
OPENAI_API_KEY=sk-your-openai-key-here
NOTION_API_KEY=secret_notion_key_here
MCP_BASE_URL=http://localhost:8081

# ログ設定
LOG_LEVEL=INFO
LOG_HUMAN=1

# Worker設定
WORKER_INTERVAL=60
```

### ポート設定

- **API**: 8060 (内部: 8000)
- **Web**: 8061 (内部: 80)
- **Worker**: バックグラウンド実行

## 📚 ドキュメント

詳細なドキュメントは `docs/` フォルダに格納されています：

- 📖 **[セットアップガイド](docs/SETUP_GUIDE.md)** - 詳細な導入手順とトラブルシューティング
- 📋 **[要件定義書](docs/REQUIREMENTS.md)** - システム要件と仕様
- 🏗️ **[詳細設計書](docs/DESIGN.md)** - アーキテクチャと技術仕様
- 📱 **[操作マニュアル](docs/USER_MANUAL.md)** - エンドユーザー向け操作ガイド
- 🔌 **[API リファレンス](docs/API_REFERENCE.md)** - API詳細仕様とサンプルコード
- 🧩 **[プラグイン開発ガイド](docs/PLUGIN_DEVELOPMENT.md)** - カスタムプラグインの作成方法

## 🧪 テスト

### テストの実行

```bash
# 基本テスト（10項目）
./tests/improved_test.sh

# 包括的テスト（18項目）
./tests/comprehensive_test.sh

# Pythonユニットテスト
pytest tests/
```

### テストファイル

- `tests/improved_test.sh` - 改修後の基本テスト
- `tests/comprehensive_test.sh` - 包括的なテストスイート
- `tests/test_classify.py` - 分類機能のユニットテスト
- `tests/test_plugins.py` - プラグインのユニットテスト
- `tests/TEST_REPORT.md` - 詳細なテスト結果レポート

## 🛠️ 開発

### プラグイン開発

新しい分類ロジックを追加する場合：

1. `src/api/plugins/` に新しいファイルを作成
2. `register()` と `classify()` 関数を実装

```python
def register() -> dict:
    return {
        "name": "custom_classifier",
        "version": "v1.0.0",
        "capabilities": ["classify"],
        "labels": ["custom"],
    }

def classify(item: dict, *, llm, notion, config) -> dict:
    # カスタム分類ロジック
    return {
        "type": "Task",
        "score": 0.8,
        "tags": ["custom"],
        "reason": "custom logic"
    }
```

### テスト実行

```bash
# コンテナ内でテスト実行
docker-compose exec api pytest

# ローカルでテスト実行
cd src
python -m pytest ../tests/
```

## 📁 プロジェクト構成

```
PRISM/
├── deploy/
│   ├── docker-compose.yml    # Docker Compose設定
│   ├── .env                  # 環境変数（要作成）
│   └── env.example          # 環境変数テンプレート
├── docker/
│   ├── Dockerfile.api       # API用Dockerfile
│   ├── Dockerfile.web       # Web用Dockerfile
│   └── Dockerfile.worker    # Worker用Dockerfile
├── src/
│   ├── api/                 # FastAPI アプリケーション
│   │   ├── main.py
│   │   ├── routers/         # API ルーター
│   │   ├── core/           # コア機能
│   │   └── plugins/        # 分類プラグイン
│   ├── worker/             # バックグラウンドワーカー
│   └── web/                # 静的Webファイル
├── config/
│   └── default.yaml        # デフォルト設定
├── tests/                  # テストファイル
└── README.md
```

## 🔍 トラブルシューティング

### よくある問題

1. **ポート競合**
   - 8060, 8061 が使用中の場合は docker-compose.yml でポート変更

2. **API キーエラー**
   - .env ファイルの API_KEY を確認
   - リクエストヘッダーに `X-API-Key` を設定

3. **コンテナ起動失敗**
   ```bash
   docker-compose logs
   docker-compose down
   docker-compose build --no-cache
   docker-compose up -d
   ```

### ログ確認

```bash
# 全サービスのログ
docker-compose logs

# 特定サービスのログ
docker-compose logs api
docker-compose logs web
docker-compose logs worker

# コンテナ名で直接ログ確認
docker logs PRISM-API
docker logs PRISM-WEB
docker logs PRISM-WORKER
```

## 📝 ライセンス

MIT License

## 🤝 貢献

1. Fork する
2. Feature ブランチを作成 (`git checkout -b feature/amazing-feature`)
3. 変更をコミット (`git commit -m 'Add amazing feature'`)
4. ブランチにプッシュ (`git push origin feature/amazing-feature`)
5. Pull Request を作成

EOF ./README.md - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初期 README

# PRISM
# PRISM
# PRISM
