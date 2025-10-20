# ./README.md - v1.0.0

# PRISM
Notionデータを Task / Knowledge / Note に自動分類し、簡易検索できる最小実装。

- Runtime: Python 3.11+, Node 20+
- Services: API (FastAPI), Web (static), Worker (batch)
- Deployment: Docker + docker-compose
- Config: `.env` + `config/default.yaml`

## 起動 / Run

```bash
cd prism/deploy
cp env.example .env
docker-compose up -d --build
```

- API: `http://localhost:8000/healthz`
- Web: `http://localhost:8080`

APIキーは `.env` の `API_KEY` を利用。デフォルトは `dev-key-change-me`。

## API 概要 / Endpoints
- `GET /healthz` … ヘルスチェック
- `POST /classify` … `{"items": [{title, body, properties?, tags?}]}` を分類
- `GET /query` … `type`, `tag`, `start`, `end` でフィルタ

## プラグイン / Plugins
`src/api/plugins/*.py` を追加するだけで拡張可能。
- 必須: `register()`, `classify(item, *, llm, notion, config)`

## テスト / Tests

```bash
docker compose -f prism/deploy/docker-compose.yml run --rm api pytest -q
```

## セキュリティ / Security
- 秘密情報は `.env` または Secret 管理を使用
- ログはJSON+人間可読の二重出力

## ライセンス / License
MIT

# EOF ./README.md - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成