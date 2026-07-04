from engine.timer_manager import TimerManager
from engine.event_bus import EventBus


class StatusEffectComponent:
    def __init__(self):
        self.effects = {} # e.g., {"Poison": Timer}, {"Stun": Timer}
    
    def add_effect(self, name:str, duration: float):
        # refresh or add new effect
        if name in self.effects:
            self.effects[name].cancel()
        self.effects[name] = TimerManager.start_timer(duration, lambda: self.remove_effect(name))
        EventBus.publish("status_applied", self.owner, name)
        
    def remove_effect(self, name: str):
        if name in self.effects: del self.effects[name]
    
    def has_effect(self, name: str):
        return name in self.effects
    
    def update(self, dt):
        # logic for DoTs (Damage over Time) would go here
        if self.has_effect("Poison"):
            #apply damage every X seconds
            pass