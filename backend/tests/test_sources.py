import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from app.models.rate import Currency
from app.services.sources.wise import WiseSource
from app.services.sources.nomad import NomadSource
from app.services.sources.confidence import ConfidenceSource


# ---------------------------------------------------------------------------
# Wise  (endpoint: wise.com/rates/live → {"source":"BRL","target":"USD","value":0.1911})
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_wise_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"source": "BRL", "target": "USD", "value": 0.1911, "time": 1234567890}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "Wise"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == round(1 / 0.1911, 4)
    assert rate.spread_pct >= 0


@pytest.mark.asyncio
async def test_wise_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("timeout"))
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None


@pytest.mark.asyncio
async def test_wise_returns_none_on_zero_value():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {"source": "BRL", "target": "USD", "value": 0, "time": 1234567890}

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = WiseSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None


# ---------------------------------------------------------------------------
# Nomad  (endpoint: api.benomad.us/forex-rates-s3/v1/calculator → {"rate":{"value":"5.23",...}})
# ---------------------------------------------------------------------------

@pytest.mark.asyncio
async def test_nomad_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "rate": {"value": "5.2336", "timestamp": "2026-03-05T00:50:00.904Z"},
        "iof": {"banking": "0.035"},
        "spread": {"default": "0.02", "custom": "0.01"},
    }

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "Nomad"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == 5.2336


@pytest.mark.asyncio
async def test_nomad_eur_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = {
        "history": [
            {"date": "2026-03-05T00:48:51.774Z", "rates": {"exchange": 6.1013}},
            {"date": "2026-03-04T23:38:37.383Z", "rates": {"exchange": 6.093}},
        ]
    }

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.EUR)

    assert rate is not None
    assert rate.currency == Currency.EUR
    assert rate.buy_rate == 6.1013


@pytest.mark.asyncio
async def test_nomad_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("connection error"))
        mock_client_cls.return_value = mock_client

        source = NomadSource()
        rate = await source.fetch(Currency.EUR)

    assert rate is None


# ---------------------------------------------------------------------------
# BCB PTAX  (endpoint: olinda.bcb.gov.br PTAX → {"value":[{"cotacaoCompra":5.20,"cotacaoVenda":5.21,...}]})
# ---------------------------------------------------------------------------

BCB_RESPONSE_USD = {
    "value": [
        {
            "paridadeCompra": 1.0,
            "paridadeVenda": 1.0,
            "cotacaoCompra": 5.2085,
            "cotacaoVenda": 5.2091,
            "dataHoraCotacao": "2026-03-04 13:07:27.146",
            "tipoBoletim": "Fechamento PTAX",
        }
    ]
}

BCB_RESPONSE_EUR = {
    "value": [
        {
            "paridadeCompra": 1.0,
            "paridadeVenda": 1.0,
            "cotacaoCompra": 6.0630,
            "cotacaoVenda": 6.0639,
            "dataHoraCotacao": "2026-03-04 13:07:27.146",
            "tipoBoletim": "Fechamento PTAX",
        }
    ]
}


@pytest.mark.asyncio
async def test_bcb_ptax_usd_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = BCB_RESPONSE_USD

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.USD)

    assert rate is not None
    assert rate.institution == "BCB PTAX (Turismo)"
    assert rate.currency == Currency.USD
    assert rate.buy_rate == 5.2091
    assert rate.sell_rate == 5.2085


@pytest.mark.asyncio
async def test_bcb_ptax_eur_success():
    mock_response = MagicMock()
    mock_response.raise_for_status = MagicMock()
    mock_response.json.return_value = BCB_RESPONSE_EUR

    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(return_value=mock_response)
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.EUR)

    assert rate is not None
    assert rate.buy_rate == 6.0639
    assert rate.sell_rate == 6.0630


@pytest.mark.asyncio
async def test_bcb_ptax_returns_none_on_error():
    with patch("httpx.AsyncClient") as mock_client_cls:
        mock_client = AsyncMock()
        mock_client.__aenter__ = AsyncMock(return_value=mock_client)
        mock_client.__aexit__ = AsyncMock(return_value=None)
        mock_client.get = AsyncMock(side_effect=Exception("timeout"))
        mock_client_cls.return_value = mock_client

        source = ConfidenceSource()
        rate = await source.fetch(Currency.USD)

    assert rate is None
