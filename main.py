import pygame
from engine.timer_manager import TimerManager
from game.camera import Camera
from game.entities.mustapha_player import MustaphaPlayer
from game.world.level import Level
from game.managers.combat_manager import CombatManager


# Constants 16:9
WIDTH, HEIGHT = 1728, 972
FPS = 60
BACKGROUND_COLOR = (30, 30, 30)

def main():
    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Basic Pygame Window")

    # Clock for controlling frame rate
    clock = pygame.time.Clock()

    camera = Camera()
    player = MustaphaPlayer()
    level = Level(player)
    level.load_current_stage()

    combat_manager = CombatManager()

    running = True
    while running:
        # Limit FPS
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update game state
        # per entity update
        entities = level.get_all_entities()
        for entity in entities:
            entity.update(dt)
        
        # cross-entity update: resolve attack/hurt collisions centrally.
        combat_manager.update(dt, entities)
        
        # world progression (wave spawns, stage clears).
        level.update(dt)

        # camera follow, locked during an active encounter.
        stage = level.current_stage if not level.is_complete else None
        if stage:
            camera.follow(player, stage.scroll_bounds, stage.is_locked)

        # timers.
        TimerManager.update(dt)

        # Draw everything
        screen.fill(BACKGROUND_COLOR)

        # (Your drawing code goes here)

        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()