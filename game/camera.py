class Camera:
    def __init__(self):
        self.x = 0

    def update(self, game_state):
        if self.locked:
            self.x = self.locked_x
        else:
            # follow player
            player = game_state.player
            self.x = player.x - game_state.screen.get_width() // 2