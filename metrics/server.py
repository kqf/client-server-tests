import asyncio
from time import sleep
from functools import lru_cache
from collections import defaultdict


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

    def __init__(self, store=None, timeout=0):
        self.store = store or defaultdict(dict)
        self.timeout = timeout

    def execute(self, message):
        data = message.split()
        command, *_ = data

        if command not in self._exposed_methods:
            return "error\nwrong command\n\n"

        method = getattr(self, command)
        return method(message)

    def put(self, message):
        sleep(self.timeout)
        try:
            _, metric_name, metric, timestamp = message.split()
            self.store[metric_name][int(timestamp)] = float(metric)
        except ValueError:
            return "error\nwrong command\n\n"
        return "ok\n\n"

    def get(self, message):
        sleep(self.timeout)
        return message


class ClientServerProtocol(asyncio.Protocol, MetricsProtocol):
    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def data_received(self, data):
        request_body = data.decode()
        print(f'Data received: {request_body}')

        response = self.execute(request_body)

        print(f'Send: {response}')
        self.transport.write(response.encode("utf-8"))

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
