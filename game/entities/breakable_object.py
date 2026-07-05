import random
import pygame

#from game.managers.asset_manager import AssetManager
from game.entities.loot import Loot
from game.entities.entity import Entity
from game.components.health_component import HealthComponent
from game.components.hurtbox_component import HurtboxComponent
from game.controllers.loot_drop_controller import LootDropController

class BreakableObject(Entity):
    """Crates, barrels, etc. Inherits from Entity."""
    def __init__(self, x: float, z: float):
        super().__init__(x, z)
        self.width, self.height = 40, 40
        self.tags.add("Breakable")
        self.add_component(HealthComponent(20))
        self.add_component(HurtboxComponent())
        self.add_component(LootDropController())

        #self.destroyed = False
        #self.explosive = False
        #self.exploded = False
        #self.box_image_file = "assets/objects/box.png"
    
    def draw(self, screen, camera_x):
        if self.destroyed:
            return
        screen_x = self.get_left() - camera_x
        screen_y = self.get_top()
        
        box_image = None # for debug
        #box_image = AssetManager.load_scaled_image(self.box_image_file,
        #                (self.width, self.height), alpha=True, smooth=True)

        if box_image:
            screen.blit(box_image, (screen_x, screen_y))
            return

        pygame.draw.rect(screen, (150,90,40),
                (screen_x, screen_y, self.width, self.height))

    def get_left(self):
        return self.x - self.width / 2

    def get_top(self):
        return self.y - self.height

    def get_rect(self):
        return pygame.Rect(self.get_left(), self.get_top(), self.width, self.height)

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.hp = 0
            self.destroyed = True

    def create_loot(self):
        if self.loot_type:
            return Loot(self.x, self.y, self.loot_type)

        roll = random.randint(1,100)
        if roll <= 50:
            return Loot(self.x, self.y, "health")
        elif roll <= 80:
            return Loot(self.x, self.y, "ammo")

        return Loot(self.x, self.y, "health")
