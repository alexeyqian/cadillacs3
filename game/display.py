import pygame

from game.settings import SCREEN_HEIGHT, SCREEN_WIDTH

ASPECT = SCREEN_WIDTH / SCREEN_HEIGHT


def _fit_size(max_width, max_height):
    """Largest size that preserves ASPECT (16:9) and fits within
    max_width x max_height."""
    if max_width / max_height > ASPECT:
        return (int(max_height * ASPECT), max_height)
    else:
        return (max_width, int(max_width / ASPECT))


def create_display():
    window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    # All game drawing targets this fixed logical-resolution surface;
    # present_screen() scales+letterboxes it into the real (fullscreen)
    # window each frame, so screen size/aspect never affects gameplay
    # math (camera, background tiling, HUD layout, ...).
    screen = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Cadillacs and Dinosaurs")
    return window, screen


def present_screen(window, screen):
    ww, wh = window.get_size()
    content_w, content_h = _fit_size(ww, wh)
    scaled = pygame.transform.smoothscale(screen, (content_w, content_h))

    # Center the scaled content, filling any leftover space (when the
    # display's aspect ratio isn't exactly 16:9) with black bars instead
    # of stretching/distorting the image.
    window.fill((0, 0, 0))
    x = (ww - content_w) // 2
    y = (wh - content_h) // 2
    window.blit(scaled, (x, y))
    pygame.display.flip()
