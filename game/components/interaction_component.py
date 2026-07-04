import math


class InteractionComponent:
    def __init__(self):
        self.interact_range = 50
        
    def try_interact(self, interactables): # list of GameObjects
        # Find closest interactable in range
        closest = None
        closest_dist = self.interact_range
        for obj in interactables:
            if obj == self.owner: continue
            dist = math.hypot(obj.x - self.owner.x, obj.z - self.owner.z)
            if dist < closest_dist:
                closest = obj
                closest_dist = dist
        if closest:
            if "breakable" in closest.tags:
                # ... trigger pickup/throw logic ...
                pass