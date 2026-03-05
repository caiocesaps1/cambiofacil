import asyncio
import json
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, RatesResponse, InstitutionType
from app.services import cache
from app.services.sources.awesomeapi import AwesomeAPISource
from app.services.sources.wise import WiseSource
from app.services.sources.nomad import NomadSource
from app.services.sources.confidence import ConfidenceSource
from app.config import settings

SOURCES = [
    AwesomeAPISource(),
    WiseSource(),
    NomadSource(),
    ConfidenceSource(),
]


def _apply_amount(rates: list[Rate], amount_brl: float) -> list[Rate]:
    result = []
    for r in rates:
        result.append(r.model_copy(update={"amount_received": round(amount_brl / r.buy_rate, 2)}))
    result.sort(key=lambda r: r.amount_received, reverse=True)
    return result


def _serialize(rates: list[Rate]) -> list[dict]:
    return [r.model_dump(mode="json") for r in rates]


def _deserialize(data: list[dict]) -> list[Rate]:
    return [Rate(**r) for r in data]


async def get_rates(currency: Currency, amount_brl: float, type_filter: str | None = None) -> RatesResponse:
    cache_key = f"rates:{currency.value}"

    # 1. Verificar cache
    cached = cache.get(cache_key)
    if cached:
        rates = _deserialize(cached)
    else:
        # 2. Buscar todas as fontes em paralelo
        results = await asyncio.gather(
            *[source.fetch(currency) for source in SOURCES],
            return_exceptions=True,
        )
        rates = [r for r in results if isinstance(r, Rate)]

        if not rates:
            raise RuntimeError("Nenhuma fonte disponível no momento.")

        # 3. Salvar no cache
        cache.set(cache_key, _serialize(rates), ttl=settings.rate_cache_ttl)

    # 4. Filtrar por tipo
    if type_filter:
        rates = [r for r in rates if r.type == type_filter]

    # 5. Calcular amount_received e ordenar
    rates = _apply_amount(rates, amount_brl)

    return RatesResponse(
        currency=currency,
        amount_brl=amount_brl,
        rates=rates,
        fetched_at=datetime.now(timezone.utc),
    )
