import pytest
from metrics.protocol import MetricsProtocol


@pytest.fixture
def protocol():
    protocol = MetricsProtocol()
    assert protocol.execute("put origin1 0.1 1") == "ok\n\n"
    assert protocol.execute("put origin1 0.1 2") == "ok\n\n"
    assert protocol.execute("put origin2 0.1 1") == "ok\n\n"
    assert protocol.execute("put origin2 0.1 2") == "ok\n\n"
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
