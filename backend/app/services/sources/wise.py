import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# Endpoint público do widget de conversão do Wise (não requer autenticação)
WISE_URL = "https://wise.com/rates/live"


class WiseSource(BaseSource):
    institution = "Wise"
    type = InstitutionType.fintech
    url = "https://wise.com/br"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency == Currency.USDC:
            return None
        target = "USD" if currency == Currency.USD else "EUR"
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    WISE_URL,
                    params={"source": "BRL", "target": target, "amount": "1000"},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # Retorna: {"source":"BRL","target":"USD","value":0.191142,"time":...}
            rate_value = float(data["value"])  # quanto de moeda estrangeira 1 BRL compra
            if rate_value <= 0:
                return None

            buy_rate = round(1 / rate_value, 4)   # quantos BRL por 1 USD/EUR
            sell_rate = round(buy_rate * 0.9975, 4)  # Wise tem spread ~0.4-0.6%
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
