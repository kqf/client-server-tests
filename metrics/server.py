import asyncio


def process_data(str):
    pass


class ClientServerProtocol(asyncio.Protocol):
    def connection_made(self, transport):
        self.transport = transport

    def data_received(self, data):
        resp = process_data(data.decode())
        self.transport.write(resp.encode())


def main():
    loop = asyncio.get_event_loop()
    coro = asyncio.start_server(
        ClientServerProtocol,
        "127.0.0.1", 10001, loop=loop
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
