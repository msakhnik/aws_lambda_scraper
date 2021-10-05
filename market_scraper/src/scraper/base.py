from abc import ABC, abstractmethod
from dataclasses import dataclass, asdict


class BaseMarketScraper(ABC):
    @abstractmethod
    def _parse_item(self, *args):
        pass

    @abstractmethod
    def get_sales(self):
        pass


@dataclass
class Item:
    data_id: int
    name: str
    discount: int
    price: int
    currency: str
    url: str
    lang: str
    timestamp: int
    type_default: str
    category: str
    market: str

    def asdict(self):
        return asdict(self)
