import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# Endpoint público do book ticker da Binance (não requer autenticação)
BINANCE_URL = "https://api.binance.com/api/v3/ticker/bookTicker"


class BinanceSource(BaseSource):
    institution = "Binance"
    type = InstitutionType.fintech
    url = "https://www.binance.com/pt-BR/buy-sell-crypto"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency != Currency.USDC:
            return None

        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    BINANCE_URL,
                    params={"symbol": "USDCBRL"},
                    headers={"User-Agent": "Mozilla/5.0"},
                )
                res.raise_for_status()
                data = res.json()

            # Retorna: {"symbol":"USDCBRL","bidPrice":"5.26590000","askPrice":"5.26660000"}
            buy_rate = round(float(data["askPrice"]), 4)   # usuário compra pelo ask
            sell_rate = round(float(data["bidPrice"]), 4)  # usuário vende pelo bid
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
