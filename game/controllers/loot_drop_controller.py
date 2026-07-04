import random


class LootDropController:
    def __init__(self):
        self.drop_table = {"HealthPotion": 0.5, "Gold": 1.0} # Item: Drop chance
        
    def on_death(self):
        # Called by SceneManager when entity dies
        for item, chance in self.drop_table.items():
            if random.random() <= chance:
                print(f"Spawning Loot: {item}")
                # In a real game, instantiate a PickupObject at self.owner.x, self.owner.z
