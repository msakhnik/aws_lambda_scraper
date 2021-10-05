import pytest
from lambda_handler import handler
from lambda_handler import prepare_cache_data


@pytest.mark.xfail
def test_handler(event, context):
    handler(event, context)


@pytest.fixture
def mock_env_path(monkeypatch):
    monkeypatch.setenv("LOCAL_CHROMIUM_PATH", "/tmp/efs/local-chromium")

@pytest.mark.skip
def test_prepare_cache_data(mock_env_path):
    prepare_cache_data()
