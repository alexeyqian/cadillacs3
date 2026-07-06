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
from game.input_snapshot import InputReader

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
    input_reader = InputReader()

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
        input = input_reader.read(pygame.key.get_pressed(), dt)
        characters = stage.get_all_characters()

        # Phase 1: decide. Reads input/AI state only, nothing moves yet,
        # so order across characters doesn't matter.
        for character in characters:
            character.update_intention(dt, input, player.x, player.z)

        # Phase 2: act. Purely local physics per character.
        for character in characters:
            character.update_movement(dt)

        # Phase 3: attack. Per-character phase-timer ticking + intent-triggered start.
        for character in characters:
            character.update_attack(dt)

        # Phase 4: reactions. Cross-character: hitbox vs hurtbox resolution.
        combat_manager.resolve(characters)

        # Sync animation to whatever state the phases above landed on.
        for character in characters:
            character.update_animation(dt)

        # world progression (wave spawns, stage clears).
        #stage.update(dt)

        camera.update(player)
        TimerManager.update(dt)
        draw(stage, screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()