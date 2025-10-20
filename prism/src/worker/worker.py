# ./src/worker/worker.py - v1.0.0
from __future__ import annotations

import asyncio
import json
import os
from typing import Any, Dict, List

from src.api.core.config import get_settings
from src.api.core.logging import configure_logging, logger
from src.api.core.llm_client import LLMClient
from src.api.core.mcp_client import MCPClient
from src.api.core.plugins import classify_item, load_plugins


async def run_once() -> List[Dict[str, Any]]:
    settings = get_settings()
    os.makedirs(settings.data_dir, exist_ok=True)
    configure_logging(level=settings.log_level, json_file_path=os.path.join(settings.data_dir, "worker.log.json"))

    registry = load_plugins(settings)
    llm = LLMClient(settings)
    mcp = MCPClient(settings)

    pages = await mcp.fetch_pages(limit=10)
    results: List[Dict[str, Any]] = []
    for p in pages:
        res = await classify_item(p, registry=registry, llm=llm, notion=mcp, config=settings)
        results.append({**p, **res})

    # Persist a simple newline-delimited JSON for demo purposes
    out_path = os.path.join(settings.data_dir, "classified.ndjson")
    with open(out_path, "a", encoding="utf-8") as f:
        for row in results:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    logger.info(f"Classified {len(results)} items")
    return results


async def main() -> None:
    await run_once()


if __name__ == "__main__":
    asyncio.run(main())

# EOF ./src/worker/worker.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成