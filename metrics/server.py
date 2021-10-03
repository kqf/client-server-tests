import asyncio
from time import sleep
from collections import defaultdict
from environs import Env


env = Env()
env.read_env()


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

        try:
            command, *_ = data
        except ValueError:
            return "error\nwrong command\n\n"

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
        try:
            _, metric_name = message.split()
        except ValueError:
            return "error\nwrong command\n\n"

        payload = "\n".join(self._ls(metric_name))
        return f"ok\n{payload}\n\n"

    def _ls(self, name):
        for metric_name, entries in self.store.items():
            if name != metric_name and name != "*":
                continue

            for timestamp, value in entries.items():
                yield f"{metric_name} {value} {timestamp}"


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


async def main():
    loop = asyncio.get_running_loop()
    addr = env("SERVER_ADDR", '127.0.0.1')
    port = env.int("PORT", 10001)
    print()
    print(f"Starting the connectin at {addr}:{port}")

    server = await loop.create_server(
        lambda: ClientServerProtocol(),
        addr,
        port,
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
