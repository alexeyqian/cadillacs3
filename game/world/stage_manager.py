from game.world.stage_config import STAGES
from game.world.stage import Stage

class StageManager:
    def __init__(self, camera, player, start_stage_id=None):
        self.camera = camera
        self.player = player
        self.enemies = []

        self.stages = STAGES
        self.current_stage_index = self._find_stage_index(start_stage_id)
        self.current_stage: Stage = None

    def load_current_stage(self):
        current_stage_data = self.stages[self.current_stage_index]
        self.current_stage = self._load_stage_from_data(self.camera, self.player, current_stage_data)
        return self.current_stage

    def advance_to_next_stage(self):
        has_next_stage = self.current_stage_index + 1 < len(self.stages)
        if not has_next_stage():
            return None

        self.current_stage_index += 1
        next_stage_data = self.stages[self.current_stage_index]
        self.current_stage = self._load_stage_from_data(self.camera, self.player, next_stage_data)
        return self.current_stage
    
    def get_current_stage(self):
        return self.current_stage

    def _find_stage_index(self, stage_id):
        if stage_id is None:
            return 0
        for index, stage in enumerate(self.stages):
            if stage["id"] == stage_id:
                return index
        raise ValueError(f"Unknown start stage id: {stage_id}")

    def _load_stage_from_data(self, camera, player, stage_data):
        camera.x = 0
        # reset player position for new stage
        start_x, start_z = stage_data["player_start"]
        player.x = start_x
        player.z = start_z
        # self._reset_entities()

        return Stage(camera, player, stage_data)

    def _reset_entities(self):
        self.enemies.clear()
        #self.weapons.clear()
        #self.projectiles.clear()
        #self.enemy_projectiles.clear()
        #self.objects.clear()
        #self.loot_items.clear()
        #self.hit_sparks.clear()
        #self.explosions.clear()
        #self.objects.clear()

        # todo: should call stage manager function
        #self.stage_clear_manager.active = False
        #self.stage_clear_manager.timer = 0
        #self.stage_clear_manager.bonus_applied = False

        # todo: should be removed, and set false as default
        #self.announcement_manager.active = False
