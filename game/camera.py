from game.settings import SCREEN_WIDTH

class Camera:
    def __init__(self):
        self.x = 0
        self.locked = False
        self.locked_x = 0

    def update(self, player):
        if self.locked:
            self.x = self.locked_x
        else:
            # follow player
            self.x = player.x - SCREEN_WIDTH // 2