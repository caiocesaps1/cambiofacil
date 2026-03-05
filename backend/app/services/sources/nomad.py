import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# Nomad expõe cotações via endpoint JSON no seu site
NOMAD_URL = "https://nomadglobal.com/api/exchange-rates"


class NomadSource(BaseSource):
    institution = "Nomad"
    type = InstitutionType.fintech
    url = "https://nomadglobal.com"

    async def fetch(self, currency: Currency) -> Rate | None:
        target = "USD" if currency == Currency.USD else "EUR"
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                res = await client.get(
                    NOMAD_URL,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Accept": "application/json",
                    },
                )
                res.raise_for_status()
                data = res.json()

            # Procurar a entrada correspondente à moeda
            entry = next(
                (item for item in data if item.get("currency") == target),
                None,
            )
            if not entry:
                return None

            buy_rate = float(entry["buy"])
            sell_rate = float(entry["sell"])
            spread_pct = round((buy_rate - sell_rate) / sell_rate * 100, 2)

            return Rate(
                institution=self.institution,
                type=self.type,
                currency=currency,
                buy_rate=round(buy_rate, 4),
                sell_rate=round(sell_rate, 4),
                spread_pct=spread_pct,
                amount_received=0.0,
                url=self.url,
                updated_at=datetime.now(timezone.utc),
            )
        except Exception:
            return None
