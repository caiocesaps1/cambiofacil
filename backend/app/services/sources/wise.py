import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

WISE_URL = "https://api.wise.com/v1/rates"


class WiseSource(BaseSource):
    institution = "Wise"
    type = InstitutionType.fintech
    url = "https://wise.com/br"

    async def fetch(self, currency: Currency) -> Rate | None:
        target = "USD" if currency == Currency.USD else "EUR"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(
                    WISE_URL,
                    params={"source": "BRL", "target": target},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # API retorna lista; pegar o primeiro item
            if not data:
                return None

            rate_value = float(data[0]["rate"])  # BRL por unidade de moeda estrangeira
            buy_rate = round(1 / rate_value, 4)  # quantos BRL por 1 USD/EUR
            sell_rate = round(buy_rate * 0.995, 4)  # estimativa de sell (Wise tem spread ~0.5%)
            spread_pct = round((buy_rate - sell_rate) / sell_rate * 100, 2)

            return Rate(
                institution=self.institution,
                type=self.type,
                currency=currency,
                buy_rate=buy_rate,
                sell_rate=sell_rate,
                spread_pct=spread_pct,
                amount_received=0.0,
                url=self.url,
                updated_at=datetime.now(timezone.utc),
            )
        except Exception:
            return None
