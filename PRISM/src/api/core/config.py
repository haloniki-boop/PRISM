
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    prism_env: str = "development"
    api_key: Optional[str] = None
    openai_api_key: Optional[str] = None
    notion_api_key: Optional[str] = None
    mcp_base_url: Optional[str] = None

    class Config:
        env_prefix = ""
        case_sensitive = False


def load_config() -> Settings:
    # Placeholder for reading YAML if needed later; environment takes precedence
    _ = Path("config/default.yaml")
    return Settings()


