import pygame
from engine.timer_manager import TimerManager
from game.settings import *
from game.colors import *
from game.camera import Camera
from game.entities.mustapha_player import MustaphaPlayer
from game.world.stage import Stage
from game.world.stage_manager import StageManager
from game.managers.combat_manager import CombatManager
from game.draw import draw
from game.input_snapshot import read_input_snapshot

def main():
    # Initialize Pygame
    pygame.init()

    # Create the window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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
        input = read_input_snapshot(pygame.key.get_pressed())
        entities = stage.get_all_entities()

        # Phase 1: decide. Reads input/AI state only, nothing moves yet,
        # so order across entities doesn't matter.
        for entity in entities:
            entity.update_intention(dt, input, player.x, player.z)

        # Phase 2: act. Purely local physics per entity.
        for entity in entities:
            entity.update_movement(dt)

        # Phase 3: attack. Per-entity phase-timer ticking + intent-triggered start.
        for entity in entities:
            entity.update_attack(dt)

        # Phase 4: reactions. Cross-entity: hitbox vs hurtbox resolution.
        combat_manager.resolve(entities)

        # Sync animation to whatever state the phases above landed on.
        for entity in entities:
            entity.update_animation(dt)

        # world progression (wave spawns, stage clears).
        #stage.update(dt)

        camera.update(player)
        TimerManager.update(dt)
        draw(stage, screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()