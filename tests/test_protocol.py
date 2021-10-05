import pytest
from metrics.protocol import MetricsProtocol


@pytest.fixture
def servers():
    return ["origin1", "origin2"]


@pytest.fixture
def measurements():
    return ["0.1 1", "0.1 2"]


@pytest.fixture
def protocol(servers, measurements):
    protocol = MetricsProtocol()
    for server, m in zip(servers, measurements):
        assert protocol.execute(f"put {server} {m}") == "ok\n\n"
    return protocol


def test_metrics_protocol(protocol):
    # Check not exposed
    assert protocol.execute("putx origin1 0.1 1") == "error\nwrong command\n\n"

    # Check wrong number of arguments
    assert protocol.execute("put") == "error\nwrong command\n\n"

    # Check wrong number of arguments
    assert protocol.execute("") == "error\nwrong command\n\n"

    # Check available data types
    assert protocol.execute("put origin 1 2 3") == "error\nwrong command\n\n"

    # Check gets no data
    assert protocol.execute("get nothing") == "ok\n\n\n"

    # Check wrong input
    assert protocol.execute("get") == "error\nwrong command\n\n"

    # Check wrong input
    assert protocol.execute("get *")
