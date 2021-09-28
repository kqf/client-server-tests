import asyncio
from metrics.server import ClientServerProtocol


def test_metrics_server(event_loop):
    coro = asyncio.start_server(
        ClientServerProtocol,
        "127.0.0.1", 10001, loop=event_loop
    )
    server = event_loop.run_until_complete(coro)

    server.close()
    event_loop.run_until_complete(server.wait_closed())
    event_loop.close()
