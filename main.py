import pygame
from engine.timer_manager import TimerManager
from game.settings import *
from game.colors import *
from game.camera import Camera
from game.entities.mustapha_player import MustaphaPlayer
from game.world.stage import Stage
from game.world.stage_manager import StageManager
from game.managers.combat_manager import CombatManager
from game.managers.collision_manager import CollisionManager
from game.managers.enemy_ai_manager import EnemyAIManager
from game.managers.audio_manager import AudioManager
from game.managers.pause_menu import PauseMenu
from game.managers.save_manager import SaveManager
from game.draw import draw
from game.input_snapshot import InputReader

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Basic Pygame Window")

    clock = pygame.time.Clock()
    camera = Camera()
    player = MustaphaPlayer(500, 500)
    stage_manager = StageManager(camera, player)
    stage = stage_manager.load_current_stage()

    combat_manager = CombatManager(stage)
    collision_manager = CollisionManager()
    enemy_ai_manager = EnemyAIManager()
    audio_manager = AudioManager()
    input_reader = InputReader()
    pause_menu = PauseMenu()

    running = True
    while running:
        # Limit FPS
        dt = clock.tick(FPS) / 1000.0  # Delta time in seconds

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pause_menu.toggle()
                elif pause_menu.is_open:
                    action = pause_menu.handle_key(event.key)
                    if action == "save":
                        SaveManager.save(player, stage)
                        pause_menu.close()
                    elif action == "load":
                        loaded_stage = SaveManager.load(player, stage_manager)
                        if loaded_stage is not None:
                            stage = loaded_stage
                            combat_manager.stage = stage
                        pause_menu.close()
                    elif action == "continue":
                        pause_menu.close()
                    elif action == "quit":
                        running = False

        if pause_menu.is_open:
            # Frozen behind the menu: redraw the last frame + overlay, skip
            # every gameplay update phase below.
            draw(stage, screen)
            pause_menu.draw(screen)
            pygame.display.flip()
            continue

        # Update game state
        input = input_reader.read(pygame.key.get_pressed(), dt)

        # World progression (wave spawns, stage clears) runs before the
        # per-character phases, so anything spawned this frame still gets a
        # full update cycle - including update_animation - before draw()
        # renders it (a fresh enemy's animation_manager has no current
        # animation at all until its first update_animation call).
        stage.update(dt)
        characters = stage.get_all_characters()

        # Assigns flank targets + attack slots for this frame, before any
        # enemy reads them in update_intention - keeps the crowd from
        # instantly mobbing the player (see EnemyAIManager).
        enemy_ai_manager.resolve(dt, player, stage.enemies)

        # Phase 1: decide. Reads input/AI state only, nothing moves yet,
        # so order across characters doesn't matter.
        for character in characters:
            character.update_intention(dt, input, player.x, player.z)

        # Phase 2: act. Purely local physics per character.
        for character in characters:
            character.update_movement(dt)

        # Phase 2.5: bodies can't overlap - push apart before attacks/combat
        # read positions, so a fast mover (e.g. a run attack) can't slide
        # clean through another character instead of bumping into them.
        collision_manager.resolve(characters)
        stage.clamp_characters_to_bounds()

        # Phase 3: attack. Per-character phase-timer ticking + intent-triggered start.
        for character in characters:
            character.update_attack(dt)

        # Phase 4: reactions. Cross-character: hitbox vs hurtbox resolution.
        # The stage exit only joins combat once there's nothing left to
        # fight - matches the "clear waves, then break through" flow - so
        # it can't be opened early just by reusing the normal combat pass.
        combat_targets = characters
        if stage.current_wave is None:
            combat_targets = characters + [stage.exit]
        combat_manager.resolve(combat_targets)

        # Sync animation to whatever state the phases above landed on.
        for character in characters:
            character.update_animation(dt)

        stage.update_clean()

        # All waves cleared and the player has reached the exit - advance to
        # the next stage. If there isn't one, just stay put (nothing else to
        # load).
        if stage.is_complete():
            next_stage = stage_manager.advance_to_next_stage()
            if next_stage is not None:
                stage = next_stage
                combat_manager.stage = stage

        camera.update(player, stage.world_width)
        TimerManager.update(dt)
        draw(stage, screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()