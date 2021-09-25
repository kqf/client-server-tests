import pytest
from metrics.client import Client


@pytest.fixture
def client():
    return Client()


def test_puts_metrics(client):
    pass
