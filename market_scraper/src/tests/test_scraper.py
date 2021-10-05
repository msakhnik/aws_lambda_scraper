from requests_html import Element, HTML
from scraper.reserved import ReservedScraper
from dataclasses import asdict


def test_reserved_parse_item(article_element):
    scraper = ReservedScraper()
    article = article_element.html.find("article")[0]
    item_data = scraper._parse_item(article)

    assert item_data.data_id == "1653C-30X"
    assert item_data.discount_price == 359
    assert item_data.currency == "UAH"
    assert item_data.regular_price == 799


def test_get_sales():
    scraper = ReservedScraper()
    for item in scraper.get_sales():
        print(item)
