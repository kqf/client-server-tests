

class HttpTransport:
    def __init__(self, transport):
        self.transport = transport

    def write(self, message):
        print("Decoding a message")
        self.transport.write(b"HTTP/1.1 200 OK\n\nHello World")
        self.transport.close()

def add_http_layer(cls):

    class HttpWrapped(cls):
        def connection_made(self, transport):
            super().connection_made(transport)
            self.transport = HttpTransport(transport)

    def create_server():
        return HttpWrapped()

    return create_server
