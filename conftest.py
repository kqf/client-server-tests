import pytest

from contextlib import closing
from metrics.client import Client


@pytest.fixture
def addr(ip="127.0.0.1", port=10001):
    return {"ip": ip, "port": port}


@pytest.fixture
def client(server, addr):
    with closing(Client(**addr, timeout=15)) as client:
        yield client
