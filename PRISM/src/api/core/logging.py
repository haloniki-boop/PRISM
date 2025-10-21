
import json
import logging
import os
from typing import Any, Dict


class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log: Dict[str, Any] = {
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
        }
        if record.exc_info:
            log["exc_info"] = self.formatException(record.exc_info)
        return json.dumps(log, ensure_ascii=False)


def configure_logging() -> None:
    level = os.getenv("LOG_LEVEL", "INFO").upper()
    human = os.getenv("LOG_HUMAN", "1") == "1"
    logging.basicConfig(level=getattr(logging, level, logging.INFO))
    root = logging.getLogger()
    # Clear existing handlers in case of reload
    root.handlers.clear()

    stream = logging.StreamHandler()
    if human:
        stream.setFormatter(logging.Formatter("[%(levelname)s] %(name)s: %(message)s"))
    else:
        stream.setFormatter(JsonFormatter())
    root.addHandler(stream)


