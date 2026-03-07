import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

OKX_URL = "https://www.okx.com/api/v5/market/ticker"


class OKXSource(BaseSource):
    institution = "OKX"
    type = InstitutionType.fintech
    url = "https://www.okx.com/pt-br/trade-spot/usdc-brl"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency != Currency.USDC:
            return None

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    OKX_URL,
                    params={"instId": "USDC-BRL"},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            ticker = data["data"][0]
            buy_rate = round(float(ticker["askPx"]), 4)   # usuário compra pelo ask
            sell_rate = round(float(ticker["bidPx"]), 4)  # usuário vende pelo bid
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
