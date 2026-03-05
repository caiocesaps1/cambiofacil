from fastapi import APIRouter, Query, HTTPException
from app.models.rate import Currency, RatesResponse
from app.services import cache
from app.services.fetcher import get_rates

router = APIRouter(prefix="/rates", tags=["rates"])

VALID_TYPES = {"bank", "fintech", "broker", "exchange_house"}


@router.get("", response_model=RatesResponse)
async def list_rates(
    currency: Currency = Query(..., description="Moeda desejada: USD ou EUR"),
    amount: float = Query(1000.0, gt=0, description="Valor em BRL a converter"),
    type: str | None = Query(None, description="Filtro: bank, fintech, broker, exchange_house"),
):
    if type is not None and type not in VALID_TYPES:
        raise HTTPException(status_code=400, detail=f"Tipo inválido. Use: {', '.join(sorted(VALID_TYPES))}")

    try:
        return await get_rates(currency, amount, type)
    except RuntimeError as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/refresh")
async def refresh_cache():
    """Força a invalidação do cache para todas as moedas."""
    for currency in Currency:
        cache.delete(f"rates:{currency.value}")
    return {"status": "ok", "message": "Cache invalidado. Próxima requisição buscará dados frescos."}
