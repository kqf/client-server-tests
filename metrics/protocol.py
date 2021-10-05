from collections import defaultdict


class MetricsProtocol:
    _exposed_methods = {
        "put",
        "get",
    }

    def __init__(self, store=None, timeout=0):
        self.store = store or defaultdict(dict)
        self.timeout = timeout

    def execute(self, message):
        data = message.split()

        try:
            command, *_ = data
        except ValueError:
            return "error\nwrong command\n\n"

        if command not in self._exposed_methods:
            return "error\nwrong command\n\n"

        method = getattr(self, command)
        return method(message)

    def put(self, message):
        try:
            _, metric_name, metric, timestamp = message.split()
            self.store[metric_name][int(timestamp)] = float(metric)
        except ValueError:
            return "error\nwrong command\n\n"
        return "ok\n\n"

    def get(self, message):
        try:
            _, metric_name = message.split()
        except ValueError:
            return "error\nwrong command\n\n"

        payload = "\n".join(self._ls(metric_name))
        return f"ok\n{payload}\n\n"

    def _ls(self, name):
        for metric_name, entries in self.store.items():
            if name != metric_name and name != "*":
                continue

            for timestamp, value in entries.items():
                yield f"{metric_name} {value} {timestamp}"
