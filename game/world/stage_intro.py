class StageIntro:
    """An optional, non-interactive moment played before a stage's normal
    gameplay begins - e.g. the player jumping in through a window. Driven
    entirely by a stage's "intro" config (see stage_config.py):

        "intro": {
            "duration": 1.5,          # seconds, required
            "animation_state": "...", # optional - a one-shot player
                                      # animation to hold on instead of the
                                      # default idle pose (needs a matching
                                      # loop=False clip in that player's
                                      # animation data)
        }

    A stage with no "intro" key just skips this entirely - is_playing is
    always False, so callers never need to special-case "no intro".
    """

    def __init__(self, player, camera, config):
        self.player = player
        self.camera = camera
        self.duration = (config or {}).get("duration", 0)
        self.animation_state = (config or {}).get("animation_state")
        self.timer = 0.0
        self.is_playing = bool(config)

        if self.is_playing:
            self._start()

    def _start(self):
        self.timer = self.duration
        self.camera.locked = True
        self.camera.locked_x = self.camera.x
        if self.animation_state:
            self.player.set_state(self.animation_state)

    def update(self, dt):
        if not self.is_playing:
            return

        self.player.update_animation(dt)

        self.timer -= dt
        if self.timer <= 0 or self._animation_finished():
            self._finish()

    def _animation_finished(self):
        if not self.animation_state:
            return False
        return (
            self.player.state == self.animation_state
            and self.player.animation_manager.is_finished()
        )

    def _finish(self):
        self.is_playing = False
        self.camera.locked = False
        if self.animation_state:
            self.player.set_state("idle")
