import random


class Camera:
    def __init__(self, screen_w, screen_h):
        self.x = 0
        self.target_x = 0
        self.shake_intensity = 0
        self.screen_w = screen_w
        self.screen_h = screen_h

    def follow(self, target_x):
        self.target_x = target_x - self.screen_w // 2

    def add_shake(self, intensity):
        self.shake_intensity = max(self.shake_intensity, intensity)

    def update(self, dt):
        self.x += (self.target_x - self.x)*5*dt
        if self.shake_intensity > 0:
            self.x += random.uniform(-self.shake_intensity, self.shake_intensity)
            self.shake_intensity = max(0, self.shake_intensity - 30 * dt)
        self.x = max(0, self.x)

    def world_to_screen(self, wx, wy, wz):
        # wy = jump height, wz = depth (up/down on screen)
        sx = wx - self.x
        # higher z = further up the screen
        # higher y = higher off ground
        sy = wz - wy
        return sx, sy
