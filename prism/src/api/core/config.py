# ./src/api/core/config.py - v1.0.0
from __future__ import annotations

import os
from functools import lru_cache
from typing import List, Optional

import yaml
from pydantic import BaseModel, Field


class ServerSettings(BaseModel):
    host: str = Field(default=os.getenv("API_HOST", "0.0.0.0"))
    port: int = Field(default=int(os.getenv("API_PORT", "8000")))
    allow_origins: List[str] = Field(default_factory=lambda: os.getenv("ALLOW_ORIGINS", "*").split(","))


class LLMSettings(BaseModel):
    provider: str = Field(default="openai")
    model: str = Field(default=os.getenv("OPENAI_MODEL", "gpt-4o-mini"))
    api_key: Optional[str] = Field(default=os.getenv("OPENAI_API_KEY"))
    temperature: float = Field(default=0.2)


class RuntimeFlags(BaseModel):
    mock_mode: bool = Field(default=os.getenv("MOCK_MODE", "true").lower() == "true")


class AppSettings(BaseModel):
    env: str = Field(default=os.getenv("ENV", "dev"))
    api_key: str = Field(default=os.getenv("API_KEY", "dev-key-change-me"))
    data_dir: str = Field(default=os.getenv("DATA_DIR", "/app/data"))
    log_level: str = Field(default=os.getenv("LOG_LEVEL", "INFO"))

    server: ServerSettings = Field(default_factory=ServerSettings)
    llm: LLMSettings = Field(default_factory=LLMSettings)
    runtime: RuntimeFlags = Field(default_factory=RuntimeFlags)

    plugins_dir: str = Field(default=os.getenv("PLUGINS_DIR", "src/api/plugins"))


def _load_yaml_config(config_path: str) -> dict:
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


@lru_cache(maxsize=1)
def get_settings(config_path: str = "config/default.yaml") -> AppSettings:
    data = _load_yaml_config(config_path)

    # YAML values override defaults; env already loaded in defaults
    server = ServerSettings(**(data.get("server", {}) or {}))
    llm = LLMSettings(**(data.get("llm", {}) or {}))
    runtime = RuntimeFlags(**(data.get("runtime", {}) or {}))

    base = AppSettings(
        **{k: v for k, v in (data.get("app", {}) or {}).items() if k in {"env", "api_key", "data_dir", "log_level", "plugins_dir"}},
        server=server,
        llm=llm,
        runtime=runtime,
    )

    # Ensure data dir exists
    os.makedirs(base.data_dir, exist_ok=True)
    return base


__all__ = ["AppSettings", "get_settings"]

# EOF ./src/api/core/config.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成