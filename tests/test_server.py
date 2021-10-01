import asyncio
import pytest
from metrics.server import ClientServerProtocol


@pytest.fixture
async def server(event_loop, addr):
    server = await event_loop.create_server(
        lambda: ClientServerProtocol(),
        addr["ip"], addr["port"])
    yield server


@pytest.mark.asyncio
async def test_metrics_server(event_loop, server, client):
    client.put("palm.cpu", 0.5, timestamp=1150864247)
    await asyncio.sleep(0.01)
    client.put("palm.cpu", 0.5, timestamp=1150864247)
