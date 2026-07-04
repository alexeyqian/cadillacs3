class SceneManager:
    """Manages level boundaries, spawning, and entity lifecycles."""
    def __init__(self, screen_w, screen_h):
        self.entities: List[GameObject] = []
        self.level = Level(2000, screen_h)
        self.particle_mgr = ParticleManager()
        
    def register_entity(self, entity: GameObject):
        self.entities.append(entity)
        
    def update(self, dt):
        # Update all entities
        for ent in self.entities:
            if ent.alive: ent.update(dt)
            
        # Level Bounds
        for ent in self.entities:
            if ent.alive: self.level.clamp_entity(ent)
            
        # Cleanup dead entities and trigger loot
        dead_entities = [e for e in self.entities if not e.alive]
        for dead in dead_entities:
            loot_ctrl = dead.get_component(LootDropController)
            if loot_ctrl: loot_ctrl.on_death()
            self.particle_mgr.spawn_burst(dead.x, dead.y, dead.z, (255,0,0), 15)
            ObjectPoolManager.return_object(dead) # Recycle if applicable
            
        self.entities = [e for e in self.entities if e.alive]
        self.particle_mgr.update(dt)