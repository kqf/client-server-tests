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


class MetricsProtocol:
    _exposed_methods = {
        "put",
        "get",
    }

    def __init__(self, store=None):
        self.store = store or {}

    def execute(self, message):
        data = message.split()
        command, *_ = data

        if command not in self._exposed_methods:
            return "error\nwrong command\n\n"

        method = getattr(self, command)
        return method(message)

    def put(self, message):
        return message

    def get(self, message):
        return message


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
        # asyncio.run(asyncio.sleep(1))

        # print('Close the client socket')
        # self.transport.close()


async def main():
    loop = asyncio.get_running_loop()

    server = await loop.create_server(
        lambda: ClientServerProtocol(),
        '127.0.0.1', 10001)

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
