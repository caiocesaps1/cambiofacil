from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import rates

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
    return {"status": "ok"}
