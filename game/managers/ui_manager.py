from engine.event_bus import EventBus


class UIManager:
    def __init__(self, player):
        self.player = player
        EventBus.subscribe("health_changed", self.on_health_changed)
        EventBus.subscribe("inventory_changed", self.on_inventory_changed)
        
    def on_health_changed(self, entity, current, maximum):
        if entity == self.player:
            print(f"UI Update: Player Health = {current}/{maximum}")

    def on_inventory_changed(self, entity, items):
        if entity == self.player:
            print(f"UI Update: Inventory = {items}")
