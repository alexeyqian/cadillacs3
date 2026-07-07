import pygame


class HurtboxComponent:
    def __init__(self, width, height, airborne_height=None):
        self.width = width
        self.height = height
        # Defaults to height (no shrink) unless configure() sets a shorter one.
        self.airborne_height = airborne_height if airborne_height is not None else height

    def configure(self, width, height, airborne_height=None):
        self.width = width
        self.height = height
        self.airborne_height = airborne_height if airborne_height is not None else height

    def get_rect(self):
        owner = self.owner
        # Top is always anchored using the full standing height, so the
        # head/torso reference point doesn't move. While airborne, the rect
        # is only extended down by the (shorter) airborne_height, excluding
        # the leg region from the hurtbox rather than shrinking from the top.
        top = owner.z - owner.y - self.height
        height = self.airborne_height if owner.y > 0 else self.height
        return pygame.Rect(owner.x - self.width // 2, top, self.width, height)
