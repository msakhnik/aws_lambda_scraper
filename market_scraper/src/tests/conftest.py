import os
import pytest
from requests_html import HTMLSession
from requests_file import FileAdapter


@pytest.fixture
def event():
    return {
  "version": "0",
  "account": "123456789012",
  "region": "us-east-2",
  "detail": {},
  "detail-type": "Scheduled Event",
  "source": "aws.events",
  "time": "2019-03-01T01:23:45Z",
  "id": "cdc73f9d-aea9-11e3-9d5a-835b769c0d9c",
  "resources": [
    "arn:aws:events:us-east-2:123456789012:rule/my-schedule"
  ]
}

@pytest.fixture
def context():
    return {}

@pytest.fixture(name="article_element")
def get_article():
    session = HTMLSession()
    session.mount('file://', FileAdapter())
    path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", 'article.html')
    url = 'file://{}'.format(path)

    return session.get(url)
