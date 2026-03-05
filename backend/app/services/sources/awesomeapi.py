import httpx
from datetime import datetime, timezone
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

AWESOME_URL = "https://economia.awesomeapi.com.br/json/last/USD-BRL,EUR-BRL"

# bid  = taxa de compra do dólar (quanto BRL paga por 1 USD) — melhor para o usuário
# ask  = taxa de venda do dólar (quanto BRL custa para comprar 1 USD)
# Usamos ask como buy_rate pois é o que o usuário paga para comprar a moeda


class AwesomeAPISource(BaseSource):
    institution = "Câmbio Oficial (BCB)"
    type = InstitutionType.bank
    url = "https://economia.awesomeapi.com.br"

    async def fetch(self, currency: Currency) -> Rate | None:
        key = "USDBRL" if currency == Currency.USD else "EURBRL"
        try:
            async with httpx.AsyncClient(timeout=10) as client:
                res = await client.get(AWESOME_URL)
                res.raise_for_status()
                data = res.json()[key]

            buy_rate = float(data["ask"])   # usuário paga esse valor por unidade
            sell_rate = float(data["bid"])  # usuário recebe esse valor ao vender
            spread_pct = round((buy_rate - sell_rate) / sell_rate * 100, 2)

            return Rate(
                institution=self.institution,
                type=self.type,
                currency=currency,
                buy_rate=round(buy_rate, 4),
                sell_rate=round(sell_rate, 4),
                spread_pct=spread_pct,
                amount_received=0.0,  # calculado no fetcher
                url="https://www.bcb.gov.br",
                updated_at=datetime.now(timezone.utc),
            )
        except Exception:
            return None
