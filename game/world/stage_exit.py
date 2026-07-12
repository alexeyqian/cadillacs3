import pygame
from game.settings import STAGE_EXIT_OPEN_DURATION
from game.entities.entity import Entity
from game.managers.asset_manager import AssetManager

# Cropped straight out of the rooftop background art at the exit's own
# position so it lines up pixel-for-pixel. A stage can supply its own via
# StageExit(exit_rect, image_path=...) - the way out doesn't have to be a
# door; it's just what stage 1 happens to use.
DEFAULT_IMAGE_PATH = "assets/backgrounds/exit.png"

# Fallback fill color, used only if the sprite file fails to load.
FALLBACK_COLOR = (120, 60, 30)


class StageExit(Entity):
    """The way out of a stage - a door, window, hatch, whatever the stage
    calls for. Starts closed; once the stage says it's ready (all waves
    cleared - see Stage.update()), the player simply walking into it
    starts its opening transition, and once fully open, walking into it
    again (Stage.is_complete()) advances to the next stage.

    Rendered as a single static image throughout - no open/close animation,
    the state machine below only drives the completion timing.

    Not a combat target - just a trigger volume the player collides with,
    so it doesn't need a HealthComponent/HurtboxComponent or any of the
    Character-shaped interface CombatManager expects from a hit target.
    """

    def __init__(self, exit_rect, image_path=None):
        rect = pygame.Rect(*exit_rect)
        # Positioned like a character: x/z is the feet/bottom-center point,
        # matching how other world entities are anchored.
        super().__init__(rect.centerx, rect.bottom)
        self.rect = rect
        self.tags.add("stage_exit")

        self.state = "closed"  # closed -> opening -> open
        self.open_timer = 0.0

        self._image = self._load_image(image_path or DEFAULT_IMAGE_PATH)

    @property
    def is_open(self):
        return self.state == "open"

    def try_open(self, collider_rect):
        """collider_rect: the player's collision rect. Starts the opening
        transition if the player is touching the exit and it's still
        closed. Call only once the stage is ready to be exited (e.g. all
        waves cleared) - this doesn't check that itself."""
        if self.state != "closed":
            return
        if collider_rect.colliderect(self.rect):
            self.state = "opening"
            self.open_timer = STAGE_EXIT_OPEN_DURATION

    def update(self, dt):
        if self.state == "opening":
            self.open_timer -= dt
            if self.open_timer <= 0:
                self.state = "open"

    def draw(self, screen, camera_x):
        position = (self.rect.x - camera_x, self.rect.y)
        if self._image:
            screen.blit(self._image, position)
        else:
            self._draw_fallback_rect(screen, camera_x)

    # --- asset loading --------------------------------------------------------

    def _load_image(self, path):
        image = AssetManager.load_image(path)
        if image is None:
            return None
        return pygame.transform.scale(image, self.rect.size)

    def _draw_fallback_rect(self, screen, camera_x):
        rect = (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, FALLBACK_COLOR, rect)
