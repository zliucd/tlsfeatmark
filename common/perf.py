from time import perf_counter

class Perf:
    def __init__(self):
        self.start = None
        self.end = None
        self.elapsed = 0.0

    def start_perf(self):
        self.start = perf_counter()

    def end_perf(self):
        self.end = perf_counter()
        self.elapsed = self.end - self.start

        return round(self.elapsed, 2)