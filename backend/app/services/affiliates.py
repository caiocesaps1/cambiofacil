# URLs de afiliado por instituição.
# Deixe None para usar a URL padrão da fonte.
# Cole seu código de afiliado em cada entrada correspondente.
#
# Como obter:
#   Wise:           https://wise.com/partners/
#   Nomad:          https://nomadglobal.com/afiliados/
#   Binance:        https://www.binance.com/pt-BR/activity/referral-entry
#   OKX:            https://www.okx.com/affiliate
#   Foxbit:         https://foxbit.com.br/afiliados/
#   Mercado Bitcoin: https://www.mercadobitcoin.com.br/indicacao/

AFFILIATE_URLS: dict[str, str | None] = {
    "Wise": None,
    # Exemplo: "Wise": "https://wise.com/invite/u/seucódigo",
    "Nomad": None,
    # Exemplo: "Nomad": "https://nomadglobal.com/?referrer=seucódigo",
    "Binance": None,
    # Exemplo: "Binance": "https://accounts.binance.com/register?ref=SEUCÓDIGO",
    "OKX": None,
    # Exemplo: "OKX": "https://www.okx.com/join/SEUCÓDIGO",
    "Foxbit": None,
    # Exemplo: "Foxbit": "https://app.foxbit.com.br/signup?ref=SEUCÓDIGO",
    "Mercado Bitcoin": None,
    # Exemplo: "Mercado Bitcoin": "https://www.mercadobitcoin.com.br/cadastro?ref=SEUCÓDIGO",
    "Confidence": None,
    "CoinGecko": None,
}


def apply_affiliate(institution: str, default_url: str) -> str:
    affiliate = AFFILIATE_URLS.get(institution)
    return affiliate if affiliate else default_url
