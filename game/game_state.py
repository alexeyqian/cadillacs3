from game.level.level import Level
from game.camera import Camera
from game.level.stage_manager import StageManager

class GameState:
    def __init__(self, screen, clock, player):
        self.screen = screen
        self.clock = clock
        self.player = player

        level = None # will be loaded at beginning
        camera = Camera()

        self.is_running = True
        self.is_paused = False
        self.keys = None

        stage_manager = StageManager()