"""
This module contains scraper of online shop
"""

import unicodedata
import os

from requests_html import HTMLSession
from typing import Dict, Any, Optional, Iterator
from scraper.base import BaseMarketScraper, Item
from requests_html import BaseSession, Element, HTMLResponse
from dataclasses import dataclass
from datetime import datetime


@dataclass
class ParsedItemData:
    data_id: int
    discount_price: int
    currency: str
    regular_price: int
    url: str
    name: str


MAX_ITEM_NUMBER = int(os.environ.get("MAX_ITEM_NUMBER", 10))
REQUEST_TIMEOUT = int(os.environ.get("REQUEST_TIMEOUT", 100))


class ReservedScraper(BaseMarketScraper):
    """Contains methods for scraping reserved.com market"""

    def __init__(self, lang: str = "ua/uk") -> None:
        self.host: str = "https://www.reserved.com"
        self.lang: str = lang
        self.market: str = "reserved"

    def _parse_item(self, article_element: Element) -> Optional[ParsedItemData]:
        data_id: int = article_element.attrs["data-sku"]
        discount_price_text: str = (
            article_element.find("p.es-discount-price").pop().text
        )
        discount_price_text = unicodedata.normalize("NFKD", discount_price_text)
        discount_price: int = int(discount_price_text.split(" ")[0])
        currency: str = discount_price_text.split(" ")[1]
        regular_price_text: str = article_element.find("p.es-regular-price").pop().text
        regular_price_text = unicodedata.normalize("NFKD", regular_price_text)

        regular_price: int = int(regular_price_text.split(" ")[0])
        links: list = article_element.find("a")
        if not links:
            return None
        url: str = links[-1].attrs["href"]
        name: str = links[-1].text

        return ParsedItemData(
            data_id, discount_price, currency, regular_price, url, name
        )

    def get_sales(
        self, type_default: str = "women", category: str = "dresses"
    ) -> Iterator[Item]:
        url: str = f"{self.host}/{self.lang}/sale/{type_default}/{category}"
        session: BaseSession = HTMLSession()
        data: HTMLResponse = session.get(url)
        data.html.render(wait=1, sleep=2, timeout=REQUEST_TIMEOUT)
        result: list = []
        counter: int = 0
        timestamp: int = int(datetime.now().timestamp())

        for i, article_element in enumerate(data.html.find("article")):
            if i == MAX_ITEM_NUMBER:
                break
            item_data = self._parse_item(article_element)

            if item_data is None:
                continue

            yield Item(
                data_id=item_data.data_id,
                name=item_data.name,
                discount=item_data.discount_price,
                price=item_data.regular_price,
                currency=item_data.currency,
                url=item_data.url,
                lang=self.lang,
                timestamp=timestamp,
                type_default=type_default,
                category=category,
                market=self.market,
            )
