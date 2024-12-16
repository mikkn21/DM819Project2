import time

class Timer:
    def __init__(self):
        self.times : list[float] = []
        self.start_time : float = None

    def start(self):
        self.start_time = time.time()

    def stop(self):
        if self.start_time is not None:
            elapsed_time = time.time() - self.start_time
            self.times.append(elapsed_time)
            self.start_time = None

    def get_total_time(self) -> float :
        return sum(self.times)

    def get_times(self) -> list[float]:
        return self.times