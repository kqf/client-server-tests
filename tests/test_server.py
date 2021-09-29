import pytest
from metrics.server import ClientServerProtocol


@pytest.fixture
async def server(event_loop, addr):
    server = await event_loop.create_server(
        lambda: ClientServerProtocol(),
        addr["ip"], addr["port"])
    yield server
    async with server:
        await server.wait_closed()


def test_metrics_server(event_loop, server, client):
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    server.close()
