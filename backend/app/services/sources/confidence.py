import httpx
from datetime import datetime, timezone, timedelta
from app.models.rate import Rate, Currency, InstitutionType
from app.services.sources.base import BaseSource

# API pública do Banco Central do Brasil - PTAX oficial
BCB_URL = "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/CotacaoMoedaDia(moeda=@moeda,dataCotacao=@dataCotacao)"


class ConfidenceSource(BaseSource):
    institution = "BCB PTAX (Turismo)"
    type = InstitutionType.exchange_house
    url = "https://www.bcb.gov.br/estabilidadefinanceira/fechamentodolar"

    async def fetch(self, currency: Currency) -> Rate | None:
        moeda = "USD" if currency == Currency.USD else "EUR"
        today = datetime.now(timezone.utc)

        # Tenta até 5 dias anteriores (cobre fins de semana e feriados)
        for delta in range(5):
            day = today - timedelta(days=delta)
            date_str = day.strftime("%m-%d-%Y")
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    res = await client.get(
                        BCB_URL,
                        params={
                            "@moeda": f"'{moeda}'",
                            "@dataCotacao": f"'{date_str}'",
                            "$format": "json",
                        },
                        headers={"User-Agent": "Mozilla/5.0"},
                    )
                    res.raise_for_status()
                    values = res.json().get("value", [])

                if not values:
                    continue

                # Pegar o boletim de fechamento PTAX (último da lista)
                entry = next(
                    (v for v in reversed(values) if "Fechamento" in v.get("tipoBoletim", "")),
                    values[-1],
                )
                buy_rate = round(float(entry["cotacaoVenda"]), 4)   # venda = usuário compra
                sell_rate = round(float(entry["cotacaoCompra"]), 4)
                spread_pct = round((buy_rate - sell_rate) / sell_rate * 100, 2)
                updated_at = datetime.fromisoformat(entry["dataHoraCotacao"].replace(" ", "T")).replace(tzinfo=timezone.utc)

                return Rate(
                    institution=self.institution,
                    type=self.type,
                    currency=currency,
                    buy_rate=buy_rate,
                    sell_rate=sell_rate,
                    spread_pct=spread_pct,
                    amount_received=0.0,
                    url=self.url,
                    updated_at=updated_at,
                )
            except Exception:
                continue
        return None
