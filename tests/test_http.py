from metrics.http import add_http_layer, HttpTransport


class MockProtocol:
    def connection_made(self, transport):
        pass


def test_adds_http_layer():
    protocol = add_http_layer(MockProtocol)()
    protocol.connection_made(None)
    assert isinstance(protocol.transport, HttpTransport)


class MockTransport:
    def write(self, message):
        self.write_params = message

    def close(self):
        self.called_close = True


def test_adds_header():
    transport = MockTransport()

    decorated = HttpTransport(transport)
    decorated.write("something")

    message_sent = transport.write_params.decode("utf-8")
    assert message_sent == "HTTP/1.1 200 OK\n\nsomething"
    assert transport.called_close
