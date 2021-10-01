import time
import socket

from collections import defaultdict


def _parse_metrics(message):
    output = defaultdict(list)
    for line in message.splitlines():
        metrics_name, metrics, timestamp = line.split()
        output[metrics_name].append(
            (float(metrics), int(timestamp))
        )
    return output


class Client:
    def __init__(self, ip="127.0.0.1", port=10001, timeout=None):
        self._sock = socket.socket()
        self._sock.connect((ip, port))
        self._sock.settimeout(timeout)

    def put(self, metrics_name, metrics, timestamp=None):
        timing = timestamp or int(time.time())
        payload = f"put {metrics_name} {metrics} {timing}\n"
        self._sock.sendall(payload.encode("utf8"))

    def get(self, metrics_name):
        self._sock.sendall(metrics_name.encode("utf8"))
        response = self._sock.recv(1024).decode("utf8")
        return _parse_metrics(response)

    def close(self):
        self._sock.close()
