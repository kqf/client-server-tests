import pytest
import socket
from contextlib import closing
from metrics.client import Client



@pytest.fixture
def addr(ip="127.0.0.1", port=10001):
    return {"ip": ip, "port": port}

 
@pytest.fixture
def server(addr):
    with socket.socket() as sock:
        sock.bind(("", 10001))
        sock.listen()   
        yield sock

@pytest.fixture
def client(server, addr):
    with closing(Client(**addr, timeout=15)) as client:
        yield client


def test_puts_metrics(client):
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    client.put("palm.cpu", 2.0, timestamp=1150864248)
    client.put("palm.cpu", 0.5, timestamp=1150864248)
    client.put("eardrum.cpu", 3, timestamp=1150864250)
    client.put("eardrum.cpu", 4, timestamp=1150864251)
    client.put("eardrum.memory", 4200000)
    print(client.get("*"))
