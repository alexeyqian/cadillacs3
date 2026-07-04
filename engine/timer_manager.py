from typing import Callable, List


class Timer:
    def __init__(self, duration: float, on_complete: Callable):
        self.time_left = duration
        self.on_complete = on_complete
        self.is_active = True

    def tick(self, dt: float):
        if not self.is_active:
            return
        self.time_left -= dt
        if self.time_left <= 0:
            self.is_active = False
            if self.on_complete:
                self.on_complete()

    def cancel(self):
        self.is_active = False


class TimerManager:
    _timers: List[Timer] = []

    @classmethod
    def start_timer(cls, duration: float, on_complete: Callable)->Timer:
        t = Timer(duration, on_complete)
        cls._timers.append(t)
        return t

    @classmethod
    def update(cls, dt: float):
        for t in cls._timers:
            t.tick(dt)
        cls._timers = [t for t in cls._timers if t.is_active]