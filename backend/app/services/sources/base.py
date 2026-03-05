from abc import ABC, abstractmethod
from app.models.rate import Rate, Currency


class BaseSource(ABC):
    institution: str
    type: str
    url: str

    @abstractmethod
    async def fetch(self, currency: Currency) -> Rate | None:
        """Busca a taxa desta fonte. Retorna None se falhar."""
        ...
