import time
import socket


class Client:
    def __init__(self, ip="127.0.0.1", port=10001, timeout=None):
        self._sock = socket.socket()
        self._sock.connect((ip, port))
        self._sock.settimeout(timeout)

    def put(self, metrics_name, metrics, timestamp=None):
        timing = timestamp or int(time.time())
        payload = f"put {metrics_name} {metrics} {timing}"
        self._sock.sendall(payload.encode("utf8"))

    def get(self, metrics_name):
        pass

    def close(self):
        self._sock.close()
