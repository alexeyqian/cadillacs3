import pygame
from game.entities.entity import Entity
from game.components.health_component import HealthComponent
from game.components.hurtbox_component import HurtboxComponent
from game.managers.asset_manager import AssetManager

# Default sprites, cropped straight out of the rooftop background art at the
# exit's own position so they line up with it pixel-for-pixel. A stage can
# supply its own via StageExit(exit_rect, closed_image_path=..., ...) - the
# way out doesn't have to be a door; it's just what stage 1 happens to use.
DEFAULT_CLOSED_IMAGE_PATH = "assets/objects/rooftop_door_closed.png"
DEFAULT_OPENING_SHEET_PATH = "assets/objects/rooftop_door_opening.png"
OPENING_FRAME_COUNT = 4

# Fallback fill colors, used only if the sprite files fail to load.
CLOSED_COLOR = (120, 60, 30)
OPENING_COLOR = (200, 140, 40)
OPEN_COLOR = (60, 160, 60)

######## stage exit ########
# How long the exit's closed -> open transition takes once the player
# lands the attack that opens it (seconds). Applies whether the stage's
# exit is dressed up as a door, a window, or anything else.
STAGE_EXIT_OPEN_DURATION = 0.5

class StageExit(Entity):
    """The way out of a stage - a door, window, hatch, whatever the stage
    calls for. Starts closed with 1 HP and a hurtbox, so the player's own
    attacks damage it exactly like any other target: CombatManager already
    knows how to resolve a hit against anything with a HealthComponent and
    a HurtboxComponent, so no bespoke hit-detection lives here. One hit is
    always enough to "kill" it (1 HP) - which here means playing its
    opening transition instead of dying. Once fully open, walking into it
    (Stage.is_complete()) advances to the next stage.

    Only takes part in combat resolution while the caller (Stage) includes
    it in the list passed to CombatManager.resolve() - see main.py, which
    only does that once the stage's waves are cleared.
    """

    def __init__(self, exit_rect, closed_image_path=None, opening_sheet_path=None):
        rect = pygame.Rect(*exit_rect)
        # Positioned like a character: x/z is the feet/bottom-center point
        # HurtboxComponent builds its rect from, not the rect's top-left.
        super().__init__(rect.centerx, rect.bottom)
        self.rect = rect
        self.alive = True
        self.tags.add("stage_exit")

        self.add_component(HealthComponent(1))
        self.add_component(HurtboxComponent(rect.width, rect.height))

        self.state = "closed"  # closed -> opening -> open
        self.open_timer = 0.0

        self._closed_image = self._load_closed_image(closed_image_path or DEFAULT_CLOSED_IMAGE_PATH)
        self._opening_frames = self._load_opening_frames(opening_sheet_path or DEFAULT_OPENING_SHEET_PATH)

    @property
    def is_open(self):
        return self.state == "open"

    # --- satisfies the interface CombatManager._react_to_hit() expects from
    # a hit target, without this object having any real attack/state
    # machinery of its own (dying IS opening - driven by `alive` below). ---

    def cancel_attack(self):
        pass

    def set_state(self, _new_state):
        pass

    def update(self, dt):
        if not self.alive and self.state == "closed":
            self.state = "opening"
            self.open_timer = STAGE_EXIT_OPEN_DURATION

        if self.state == "opening":
            self.open_timer -= dt
            if self.open_timer <= 0:
                self.state = "open"

    def draw(self, screen, camera_x):
        image = self._current_image()
        position = (self.rect.x - camera_x, self.rect.y)
        if image:
            screen.blit(image, position)
        else:
            self._draw_fallback_rect(screen, camera_x)

    # --- frame selection ----------------------------------------------------

    def _current_image(self):
        if self.state == "closed":
            return self._closed_image
        if not self._opening_frames:
            return None
        if self.state == "open":
            return self._opening_frames[-1]
        return self._opening_frames[self._opening_frame_index()]

    def _opening_frame_index(self):
        progress = 1 - max(0.0, self.open_timer) / STAGE_EXIT_OPEN_DURATION
        index = int(progress * len(self._opening_frames))
        return min(index, len(self._opening_frames) - 1)

    # --- asset loading --------------------------------------------------------

    def _load_closed_image(self, path):
        image = AssetManager.load_image(path)
        if image is None:
            return None
        return pygame.transform.scale(image, self.rect.size)

    def _load_opening_frames(self, path):
        sheet = AssetManager.load_image(path)
        if sheet is None:
            return []

        frame_width = sheet.get_width() // OPENING_FRAME_COUNT
        frame_height = sheet.get_height()
        frames = []
        for i in range(OPENING_FRAME_COUNT):
            frame = sheet.subsurface((i * frame_width, 0, frame_width, frame_height))
            frames.append(pygame.transform.scale(frame, self.rect.size))
        return frames

    def _draw_fallback_rect(self, screen, camera_x):
        color = {"closed": CLOSED_COLOR, "opening": OPENING_COLOR, "open": OPEN_COLOR}[self.state]
        rect = (self.rect.x - camera_x, self.rect.y, self.rect.width, self.rect.height)
        pygame.draw.rect(screen, color, rect)
