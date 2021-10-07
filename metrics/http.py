

class HttpTransport:
    def __init__(self, transport):
        self.transport = transport

    def write(self, message):
        print("Decoding a message")
        encapsulated = f"HTTP/1.1 200 OK\n\n{message.decode('utf-8')}"
        self.transport.write(encapsulated.encode("utf-8"))
        self.transport.close()


def add_http_layer(cls):
    """
    Adds an additional http-like layer in order to be able to run on Heroku
    """
    class HttpWrapped(cls):
        def connection_made(self, transport):
            super().connection_made(transport)
            self.transport = HttpTransport(transport)

    def create_server():
        return HttpWrapped()

    return create_server
