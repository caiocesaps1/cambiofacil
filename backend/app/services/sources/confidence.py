import httpx
from bs4 import BeautifulSoup
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

CONFIDENCE_URL = "https://www.confidence.com.br/cambio"


class ConfidenceSource(BaseSource):
    institution = "Confidence"
    type = InstitutionType.exchange_house
    url = "https://www.confidence.com.br/cambio"

    async def fetch(self, currency: Currency) -> Rate | None:
        target = "dolar" if currency == Currency.USD else "euro"
        try:
            async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
                res = await client.get(
                    CONFIDENCE_URL,
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
                        "Accept-Language": "pt-BR,pt;q=0.9",
                    },
                )
                res.raise_for_status()

            soup = BeautifulSoup(res.text, "html.parser")

            # Localizar bloco da moeda pelo slug (dolar / euro)
            block = soup.find(attrs={"data-currency": target}) or soup.find(
                "div", class_=lambda c: c and target in c.lower()
            )
            if not block:
                return None

            # Extrair valores de compra e venda
            buy_el = block.find(attrs={"data-type": "buy"}) or block.find(class_=lambda c: c and "buy" in c.lower())
            sell_el = block.find(attrs={"data-type": "sell"}) or block.find(class_=lambda c: c and "sell" in c.lower())

            if not buy_el or not sell_el:
                return None

            buy_rate = float(buy_el.get_text(strip=True).replace(",", ".").replace("R$", "").strip())
            sell_rate = float(sell_el.get_text(strip=True).replace(",", ".").replace("R$", "").strip())
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
