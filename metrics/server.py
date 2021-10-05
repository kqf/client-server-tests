import asyncio
from environs import Env


from metrics.http import add_http_layer
from metrics.protocol import MetricsProtocol


env = Env()
env.read_env()


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
        print(f'The transport type is {type(self.transport)}')
        self.transport.write(response.encode("utf-8"))


async def main():
    loop = asyncio.get_running_loop()
    addr = env("SERVER_ADDR", '127.0.0.1')
    port = env.int("PORT", 10001)
    print()
    print(f"Starting the connectin at {addr}:{port}")

    server = await loop.create_server(
        # Start on heroku
        add_http_layer(ClientServerProtocol),
        addr,
        port,
    )

    async with server:
        await server.serve_forever()


if __name__ == '__main__':
    asyncio.run(main())
