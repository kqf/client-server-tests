import asyncio
from functools import lru_cache


@lru_cache
def process_data(message):
    if message.startswith("get"):
        _, metric_name = message.split()
        return metric_name

    if message.startswith("put"):
        command, metric_name, metric, timestamp = message.split()
        return {(metric_name, timestamp): metric}

    raise NotImplementedError("Other commands are not implemented")


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))

        print('Send: {!r}'.format(message))
        self.transport.write(data)

        print('Close the client socket')
        self.transport.close()


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(
        ClientServerProtocol,
        "127.0.0.1", 10001
    )
    server = loop.run_until_complete(coro)
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()


if __name__ == '__main__':
    main()
