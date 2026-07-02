from game.level.level import Level
from game.camera import Camera

class GameState:
    def __init__(self, screen, clock, player):
        self.screen = screen
        self.clock = clock
        self.player = player
        
        level = Level()
        camera = Camera()

        self.is_running = True
        self.is_paused = False
        self.keys = None