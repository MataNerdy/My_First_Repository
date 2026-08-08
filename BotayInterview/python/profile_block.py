import time


class ProfileBlock:
    def __init__(self, name: setattr):
        self.name = name
        self._start = None
        self._durations = []

    def __enter__(self):
        self._start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        duration = time.perf_counter()-self._start
        self._durations.append(duration)
        self._start = None
        return False

    def get_stats(self):
        if not self._durations:
            return {
                "count": 0,
                "min": None,
                "max": None,
                "avg": None,
            }
        return {
            "count": f"{len(self._durations)}",
            "min": f"{min(self._durations):.4f}",
            "max": f"{max(self._durations):.4f}",
            "avg": f"{round((sum(self._durations)/len(self._durations)),4)}",
        }

with ProfileBlock("math section") as block:
    time.sleep(0.1)
    result = 2**10
print("start")
print(block.get_stats())
print("stop")
