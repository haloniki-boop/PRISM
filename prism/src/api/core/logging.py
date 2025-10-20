# ./src/api/core/logging.py - v1.0.0
from __future__ import annotations

import json
import os
import sys
from typing import Any, Dict

from loguru import logger


def configure_logging(level: str = "INFO", json_file_path: str | None = None) -> None:
    logger.remove()

    # Human-readable to stderr
    logger.add(sys.stderr, level=level, colorize=True, backtrace=False, diagnose=False,
               format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>")

    # JSON structured log to file
    if json_file_path:
        def serialize(record: Dict[str, Any]) -> str:
            r = record.copy()
            # Convert record to JSON-friendly dict
            out = {
                "timestamp": record.get("time").isoformat() if record.get("time") else None,
                "level": record.get("level").name if record.get("level") else None,
                "message": record.get("message"),
                "module": record.get("name"),
                "function": record.get("function"),
                "line": record.get("line"),
                "extra": record.get("extra", {}),
            }
            return json.dumps(out, ensure_ascii=False)

        logger.add(json_file_path, level=level, serialize=False, backtrace=False, diagnose=False, format=serialize)


__all__ = ["configure_logging", "logger"]

# EOF ./src/api/core/logging.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成