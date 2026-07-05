from engine.timer_manager import TimerManager


class CharacterController:
    """The Master State Machine. Prevents illegal actions."""
    def __init__(self):
        self.state = "idle"
        self.hit_stun_timer = None

    def can_act(self):
        return self.state in ["idle", "walk", "run", "jump", "attack", "chase"]

    def set_state(self, new_state: str):
        if self.state == "dead": return
        self.state = new_state

    def stun(self, duration):
        if self.hit_stun_timer:
            self.hit_stun_timer.cancel()
        self.set_state("hit")
        self.hit_stun_timer = TimerManager.start_timer(duration, lambda: self.set_state("idle"))