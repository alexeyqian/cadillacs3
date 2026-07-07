import pygame
from game.camera import world_to_screen


class FloatingText:
    RISE_SPEED = 60  # world "height" units per second - see world_to_screen

    def __init__(self, text, x, z, color=(255, 220, 60), duration=0.8):
        self.text = text
        self.x = x
        self.z = z
        self.y = 0.0
        self.color = color
        self.duration = duration
        self.age = 0.0

    def update(self, dt):
        self.age += dt
        self.y += self.RISE_SPEED * dt

    @property
    def is_expired(self):
        return self.age >= self.duration

    @property
    def alpha(self):
        remaining = 1.0 - (self.age / self.duration)
        return max(0, min(255, int(255 * remaining)))


class FloatingTextManager:
    """World-space floating text (score popups, etc.) - spawn, update, draw."""

    def __init__(self):
        self._texts = []
        self._font = None

    def spawn(self, text, x, z, color=(255, 220, 60)):
        self._texts.append(FloatingText(text, x, z, color))

    def update(self, dt):
        for t in self._texts:
            t.update(dt)
        self._texts = [t for t in self._texts if not t.is_expired]

    def draw(self, screen, camera_x):
        if not self._texts:
            return
        if self._font is None:
            self._font = pygame.font.SysFont(None, 26)

        for t in self._texts:
            surface = self._font.render(t.text, True, t.color)
            surface.set_alpha(t.alpha)
            screen_x, screen_y = world_to_screen(t.x, t.y, t.z, camera_x)
            screen.blit(surface, (screen_x - surface.get_width() // 2, screen_y))
