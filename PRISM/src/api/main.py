from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import health, classify, query
from .core.logging import configure_logging


configure_logging()

app = FastAPI(title="PRISM API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router)
app.include_router(classify.router)
app.include_router(query.router)


@app.get("/")
def root():
    return {"ok": True, "service": "prism", "version": "1.0.0"}

