from engine.event_bus import EventBus


class AudioManager:
    def __init__(self):
        # Subscribe to game events
        EventBus.subscribe("hit_landed", self.on_hit_landed)
        EventBus.subscribe("entity_died", self.on_entity_died)
        
    def on_hit_landed(self, target, amount, knockback):
        print(f"Playing Sound: Punch_Hit (Damage: {amount})")
        
    def on_entity_died(self, entity):
        print("Playing Sound: Death_Scream")