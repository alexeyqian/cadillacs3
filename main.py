import pygame
from engine.timer_manager import TimerManager
from game.camera import Camera
from game.entities.mustapha_player import MustaphaPlayer
from game.world.stage import Stage
from game.world.stage_manager import StageManager
from game.managers.combat_manager import CombatManager
from game.draw import draw

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
    player = MustaphaPlayer(500, 500)
    stage_manager = StageManager(camera, player)
    stage = stage_manager.load_current_stage()

    combat_manager = CombatManager()

    running = True
    while running:
        # Limit FPS
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        # Update game state
        # per entity update
        # player.get_component(InputController).handle_input(keys)?
        entities = stage_manager.get_all_entities()
        for entity in entities:
            entity.update(dt)
        
        # cross-entity update: resolve attack/hurt collisions centrally.
        #combat_manager.update(dt, entities)
        
        # world progression (wave spawns, stage clears).
        #stage.update(dt)

        camera.update(player)

        # timers.
        TimerManager.update(dt)

        # Draw everything
        screen.fill(BACKGROUND_COLOR)
        draw(stage, screen)
        # Update the display
        pygame.display.flip()

    # Clean up
    pygame.quit()

if __name__ == "__main__":
    main()