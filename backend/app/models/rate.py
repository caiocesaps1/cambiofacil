from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class Currency(str, Enum):
    USD = "USD"
    EUR = "EUR"


class InstitutionType(str, Enum):
    bank = "bank"
    fintech = "fintech"
    broker = "broker"
    exchange_house = "exchange_house"


class Rate(BaseModel):
    institution: str
    type: InstitutionType
    currency: Currency
    buy_rate: float
    sell_rate: float
    spread_pct: float
    amount_received: float  # quanto o usuário recebe na moeda estrangeira
    url: str
    updated_at: datetime


class RatesResponse(BaseModel):
    currency: Currency
    amount_brl: float
    rates: list[Rate]
    fetched_at: datetime
