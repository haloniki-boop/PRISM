# ./src/api/main.py - v1.0.0
from __future__ import annotations

import os
from typing import List

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .core.config import get_settings
from .core.logging import configure_logging, logger
from .routers import health as health_router
from .routers import classify as classify_router
from .routers import query as query_router
from .routers import sync as sync_router


app = FastAPI(title="PRISM API", version="v1.0.0")


settings = get_settings()
log_json_path = os.path.join(settings.data_dir, "app.log.json")
configure_logging(level=settings.log_level, json_file_path=log_json_path)

# CORS
origins: List[str] = settings.server.allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(health_router.router)
app.include_router(classify_router.router)
app.include_router(query_router.router)
app.include_router(sync_router.router)


# EOF ./src/api/main.py - v1.0.0
# 修正履歴:
# - 2025-10-20 v1.0.0: 初版作成