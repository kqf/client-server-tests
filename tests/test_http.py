from metrics.http import add_http_layer, HttpTransport


class MockProtocol:
    def connection_made(self, transport):
        pass


def test_adds_http_layer():
    protocol = add_http_layer(MockProtocol)()
    protocol.connection_made(None)
    assert isinstance(protocol.transport, HttpTransport)
