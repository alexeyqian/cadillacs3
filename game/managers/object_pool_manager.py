from typing import List, Dict
from game.entities.game_object import GameObject


class ObjectPoolManager:
    """Recycles objects to prevent garbage collection spikes."""
    _pools: Dict[str, List[GameObject]] = {}
    
    @classmethod
    def get_object(cls, obj_type: str) -> GameObject:
        if obj_type in cls._pools and cls._pools[obj_type]:
            obj = cls._pools[obj_type].pop()
            obj.alive = True
            return obj
        # If pool is empty, create new (requires a factory/mapping in real code)
        #return Projectile(0,0,0,0,10) # Example fallback
        return None
    
    @classmethod
    def return_object(cls, obj: GameObject):
        obj.alive = False
        obj_type = list(obj.tags)[0] if obj.tags else "generic"
        cls._pools.setdefault(obj_type, []).append(obj)