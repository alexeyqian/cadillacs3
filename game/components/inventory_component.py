from engine.event_bus import EventBus


class InventoryComponent:
    def __init__(self):
        self.items = [] # e.g., ["HealthPotion", "ThrowingKnife"]
    
    def add_item(self, item_name: str):
        self.items.append(item_name)
        EventBus.puslish("inventory_changed", self.owner, self.items)
        
    def use_item(self, item_name: str):
        if item_name in self.items:
            self.items.remove(item_name)
            EventBus.publish("item_used", self.owner, item_name)
            return True
        return False
