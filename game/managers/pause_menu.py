import pygame
from game.colors import WHITE_COLOR, YELLOW_COLOR

# (label shown on screen, action returned when confirmed)
MENU_OPTIONS = [
    ("Save Game", "save"),
    ("Load Game", "load"),
    ("Continue", "continue"),
    ("Quit", "quit"),
]


class PauseMenu:
    """A simple keyboard-navigable pause overlay. main.py drives it:
    - toggle() on ESC
    - handle_key() for each KEYDOWN while it's open
    - draw() every frame it's open
    It only tracks menu state (open? which option is highlighted?) - it
    doesn't know how to save/load/continue/quit; main.py acts on the
    action string handle_key() returns.
    """

    def __init__(self):
        self.is_open = False
        self.selected_index = 0
        self._title_font = None
        self._option_font = None

    def toggle(self):
        self.is_open = not self.is_open
        self.selected_index = 0

    def close(self):
        self.is_open = False

    def handle_key(self, key):
        """Call once per KEYDOWN event while is_open. Returns the chosen
        action ("save"/"load"/"continue"/"quit") if this key confirmed a
        selection, otherwise None."""
        if key in (pygame.K_UP, pygame.K_w):
            self._move_selection(-1)
        elif key in (pygame.K_DOWN, pygame.K_s):
            self._move_selection(1)
        elif key in (pygame.K_RETURN, pygame.K_KP_ENTER):
            return MENU_OPTIONS[self.selected_index][1]
        return None

    def _move_selection(self, direction):
        self.selected_index = (self.selected_index + direction) % len(MENU_OPTIONS)

    def draw(self, screen):
        self._ensure_fonts()
        self._draw_dim_overlay(screen)
        self._draw_title(screen)
        self._draw_options(screen)

    def _ensure_fonts(self):
        if self._title_font is None:
            self._title_font = pygame.font.SysFont(None, 64, bold=True)
        if self._option_font is None:
            self._option_font = pygame.font.SysFont(None, 40)

    def _draw_dim_overlay(self, screen):
        overlay = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        screen.blit(overlay, (0, 0))

    def _draw_title(self, screen):
        surface = self._title_font.render("PAUSED", True, WHITE_COLOR)
        x = screen.get_width() // 2 - surface.get_width() // 2
        y = screen.get_height() // 2 - 120
        screen.blit(surface, (x, y))

    def _draw_options(self, screen):
        start_y = screen.get_height() // 2 - 20
        row_height = 50
        for i, (label, _action) in enumerate(MENU_OPTIONS):
            is_selected = i == self.selected_index
            text = f"> {label}" if is_selected else f"  {label}"
            color = YELLOW_COLOR if is_selected else WHITE_COLOR

            surface = self._option_font.render(text, True, color)
            x = screen.get_width() // 2 - surface.get_width() // 2
            y = start_y + i * row_height
            screen.blit(surface, (x, y))
