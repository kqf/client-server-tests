import pytest
import asyncio
from metrics.server import ClientServerProtocol


@pytest.fixture
def server(event_loop, addr):
    coro = asyncio.start_server(ClientServerProtocol, addr["ip"], addr["port"])
    server = event_loop.run_until_complete(coro)
    yield server
    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()


def test_metrics_server(event_loop, server, client):
    client.put("palm.cpu", 0.5, timestamp=1150864247)
