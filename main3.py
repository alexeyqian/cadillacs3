import pygame

from game.settings import FPS
from game.display import create_display, present_screen
from game.game_state import GameState
from game.entities.mustapha_player import MustaphaPlayer

from game import draw

def main():
    pygame.init()
    window, screen = create_display()
    clock = pygame.time.Clock()

    camera = Camera()
    level_manager = LevelManager()
    combat_manager = CombatManager()

    player = MustaphaPlayer()
    # game_manager
    game_state = GameState(screen, clock, player)
    
    level_manager.start_first_stage(game_state)

    # ui_manager = UIManager(player)

    # accumulator for fixed update (physics)
    # fixed_dt = 1.0/FPS
    # accumulator = 0.0

    while game_state.is_running:
        # 1. calculate delta time
        raw_dt = clock.tick(FPS) / 1000.0
        # Prevent spiral of death (e.g., if game freezes)
        raw_dt = min(raw_dt, 0.25)
        # scaled_dt = frame_dt * GameFeelManager.time_scale

        for event in pygame.event.get():
            # game closed
            if event.type == pygame.QUIT:
                game_state.running = False
                continue
            # escape key pressed
            # todo: show system menu for eacape key
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    game_state.is_running = False
                    continue

        if not game_state.running:
            break
        
        # order:
        # intention before movement
        # timers before movement
        # movement before combat
        # combat before reactions

        # 2. handle input & intention
        game_state.keys = pygame.key.get_pressed()
        player.get_component(InputController).handle_input(game_state.keys)
        #for enemy in enemies:
        #    enemy.update_intent() # ai decides what to do
        # player.update_intent()
        # 3. Timers and cooldowns
        TimerManager.update(raw_dt)
        
        # 4. Movement/Physics & combat
        # accumulate time to run physics at a constant rate
        accumulator += scaled_dt
        while accumulator >= fixed_dt:
            # movement & physics
            player.update_physics(fixed_dt)
            for enemy in enemies:
                enemy.update_physics(fixed_dt)
            # combat resolution
            for hitbox in active_hitboxes:
                hitbox.check_collision([player] + enemies)
                
            accumulator -= fixed_dt

        # 5. Reactions/Gamefeel
        # ...
        
        # ...
        stage_manager.update(raw_dt)

        # camera.follow(player.x)
        # camera.update(raw_dt)
        game_state.camera.update(game_state)
        draw(game_state)
        present_screen(window, screen)

    pygame.quit()


if __name__ == "__main__":
    main()