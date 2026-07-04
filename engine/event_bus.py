from typing import Callable, List

class EventBus:
    _listeners = {}
    
    @classmethod
    def subscribe(cls, event_name: str, callback:Callable):
        cls._listeners.setdefault(event_name, []).append(callback)
    
    @classmethod
    def publish(cls, event_name: str, *args):
        if event_name in cls._listeners:
            for cb in cls._listeners[event_name]:
                cb(*args)
    