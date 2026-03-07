from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rates
from app.services.fetcher import get_source_status
from app.services import cache as cache_module

app = FastAPI(
    title="CâmbioFácil API",
    description="Buscador de taxas de câmbio (USD e EUR)",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(rates.router)


@app.get("/health")
async def health():
    source_status = get_source_status()
    sources = {}
    for name, s in source_status.items():
        if s["last_ok"] is None and s["last_error"] is None:
            status = "unknown"
        elif s["last_error"] and (s["last_ok"] is None or s["last_error"] > s["last_ok"]):
            status = "error"
        else:
            status = "ok"
        sources[name] = {
            "status": status,
            "last_ok": s["last_ok"].isoformat() if s["last_ok"] else None,
            "last_error": s["last_error"].isoformat() if s["last_error"] else None,
            "error": s["error"],
        }

    any_ok = any(s["status"] == "ok" for s in sources.values())
    all_unknown = all(s["status"] == "unknown" for s in sources.values())
    overall = "ok" if any_ok else ("unknown" if all_unknown else "degraded")

    return {
        "status": overall,
        "cache": "redis" if cache_module.is_redis() else "memory",
        "sources": sources,
    }
