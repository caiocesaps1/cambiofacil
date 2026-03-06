import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# Endpoint público do Mercado Bitcoin (não requer autenticação)
MB_URL = "https://www.mercadobitcoin.net/api/USDC/ticker/"


class MercadoBitcoinSource(BaseSource):
    institution = "Mercado Bitcoin"
    type = InstitutionType.fintech
    url = "https://www.mercadobitcoin.com.br"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency != Currency.USDC:
            return None

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    MB_URL,
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # Retorna: {"ticker":{"buy":"5.26380000","sell":"5.26680000","last":"5.26430000",...}}
            ticker = data["ticker"]
            buy_rate = round(float(ticker["buy"]), 4)
            sell_rate = round(float(ticker["sell"]), 4)
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
