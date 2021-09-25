import pytest
from contextlib import closing
from metrics.client import Client


@pytest.fixture
def client():
    with closing(Client(ip="127.0.0.1", port=10001)) as client:
        yield client


def test_puts_metrics(client):
    pass
