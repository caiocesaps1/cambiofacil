import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# Endpoint público da CoinGecko (free tier, sem autenticação)
COINGECKO_URL = "https://api.coingecko.com/api/v3/simple/price"


class CoinGeckoSource(BaseSource):
    institution = "CoinGecko"
    type = InstitutionType.fintech
    url = "https://www.coingecko.com/pt/moedas/usd-coin"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency != Currency.USDC:
            return None

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    COINGECKO_URL,
                    params={"ids": "usd-coin", "vs_currencies": "brl"},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # Retorna: {"usd-coin":{"brl":5.24}}
            buy_rate = round(float(data["usd-coin"]["brl"]), 4)
            if buy_rate <= 0:
                return None

            # CoinGecko retorna preço de mercado sem distinção compra/venda
            sell_rate = round(buy_rate * 0.999, 4)  # 0.1% spread estimado
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
