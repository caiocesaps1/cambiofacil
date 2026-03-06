import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# API interna do Nomad (descoberta via análise do site nomadglobal.com)
NOMAD_BASE = "https://api.benomad.us/forex-rates-s3/v1"


class NomadSource(BaseSource):
    institution = "Nomad"
    type = InstitutionType.fintech
    url = "https://nomadglobal.com"

    async def fetch(self, currency: Currency) -> Rate | None:
        if currency == Currency.USDC:
            return None
        try:
            async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
                if currency == Currency.USD:
                    # /calculator dá a taxa USD mais atualizada
                    res = await client.get(
                        f"{NOMAD_BASE}/calculator",
                        headers={"User-Agent": "Mozilla/5.0", "Origin": "https://nomadglobal.com"},
                    )
                    res.raise_for_status()
                    data = res.json()
                    buy_rate = round(float(data["rate"]["value"]), 4)
                else:
                    # /exchanges/EUR_BRL retorna histórico; pegar o mais recente
                    res = await client.get(
                        f"{NOMAD_BASE}/exchanges/EUR_BRL",
                        headers={"User-Agent": "Mozilla/5.0", "Origin": "https://nomadglobal.com"},
                    )
                    res.raise_for_status()
                    data = res.json()
                    buy_rate = round(float(data["history"][0]["rates"]["exchange"]), 4)

            # Nomad cobra spread padrão de ~2% sobre a taxa comercial
            spread = float(data.get("spread", {}).get("default", "0.02")) if currency == Currency.USD else 0.02
            sell_rate = round(buy_rate / (1 + spread), 4)
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
