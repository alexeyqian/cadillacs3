class WarningManager:
    """Shows a short-lived message (e.g. "WAVE OF ENEMIES") centered on
    screen, auto-hiding itself after `duration` seconds."""

    def __init__(self):
        self.message = None
        self.timer = 0.0

    def show(self, message, duration=2.0):
        self.message = message
        self.timer = duration

    def update(self, dt):
        if self.timer <= 0:
            return
        self.timer -= dt
        if self.timer <= 0:
            self.timer = 0.0
            self.message = None

    @property
    def active(self):
        return self.message is not None and self.timer > 0
