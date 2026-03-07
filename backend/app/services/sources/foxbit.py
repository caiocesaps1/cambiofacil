import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

FOXBIT_URL = "https://api.foxbit.com.br/rest/v3/markets/usdcbrl/orderbook"


class FoxbitSource(BaseSource):
    institution = "Foxbit"
    type = InstitutionType.fintech
    url = "https://foxbit.com.br/buy-crypto/usdc/"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency != Currency.USDC:
            return None

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    FOXBIT_URL,
                    params={"depth": "1"},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # Retorna: {"asks": [["5.277", "15237..."]], "bids": [["5.2748", "400..."]]}
            buy_rate = round(float(data["asks"][0][0]), 4)   # usuário compra pelo ask
            sell_rate = round(float(data["bids"][0][0]), 4)  # usuário vende pelo bid
            if buy_rate <= 0:
                return None

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
