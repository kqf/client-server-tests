import pytest

from contextlib import closing
from metrics.client import Client


@pytest.fixture
def client(server, addr):
    with closing(Client(**addr, timeout=15)) as client:
        yield client
