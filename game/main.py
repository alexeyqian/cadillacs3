import pygame

from game.settings import FPS
from game.display import create_display, present_screen
from game.game_state import GameState
from game.entities.mustapha_player import MustaphaPlayer

from game import draw

# os.environ["SDL_VIDEO_WINDOW_POS"] = "0,0"

def main():
    pygame.init()
    window, screen = create_display()
    clock = pygame.time.Clock()
    player = MustaphaPlayer()
    game_state = GameState(screen, clock, player)
    game_state.stage_manager.load_current_stage(game_state)

    while game_state.is_running:
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

        game_state.keys = pygame.key.get_pressed()
        
        for character in game_state.characters:
            character.update()

        game_state.camera.update(game_state)
        draw(game_state)
        present_screen(window, screen)
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()