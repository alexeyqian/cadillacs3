from game.entities.breakable_object import BreakableObject
# from game.entities.explosive_barrel import ExplosiveBarrel
from game.entities.weapon import Weapon
from game.world.level_config import STAGES

class Level:
    def __init__(self, start_stage_id=None):
        self.stages = STAGES
        self.current_stage_index = self._find_stage_index(start_stage_id)

    def load_current_stage(self, game_state):
        current_stage_data = self.stages[self.current_stage_index]
        self._load_stage_from_data(game_state, current_stage_data)

    def advance_to_next_stage(self, game_state):
        has_next_stage = self.current_stage_index + 1 < len(self.stages)
        if not has_next_stage():
            return False

        self.current_stage_index += 1
        next_stage_data = self.stages[self.current_stage_index]
        self._load_stage_from_data(game_state, next_stage_data)
        return True

    def _find_stage_index(self, stage_id):
        if stage_id is None:
            return 0
        for index, stage in enumerate(self.stages):
            if stage["id"] == stage_id:
                return index
        raise ValueError(f"Unknown start stage id: {stage_id}")

    def _load_stage_from_data(self, game_state, stage_data):
        game_state.level = Level(stage_data)

        # Do not create a new Player. Keep the same player so lives, score,
        # and weapon behavior can be decided intentionally later.
        start_x, start_y = stage_data["player_start"]
        game_state.player.reset_for_stage_start(start_x, start_y)

        game_state.camera.x = 0

        game_state.enemies.clear()
        game_state.weapons.clear()
        game_state.projectiles.clear()
        game_state.enemy_projectiles.clear()
        game_state.objects.clear()
        game_state.loot_items.clear()
        game_state.hit_sparks.clear()
        game_state.floating_texts.clear()
        game_state.explosions.clear()

        game_state.weapons.extend(self._create_weapons(stage_data))
        game_state.objects.extend(self._create_objects(stage_data))

        # todo: should call stage manager function
        game_state.stage_clear_manager.active = False
        game_state.stage_clear_manager.timer = 0
        game_state.stage_clear_manager.bonus_applied = False

        # todo: should be removed, and set false as default
        game_state.announcement_manager.active = False

    def _create_weapons(self, stage_data):
        return [
            Weapon(wc["x"], wc["y"], wc["type"])
            for wc in stage_data["weapons"]
        ]

    def _create_objects(self, stage_data):
        objects = []
        for oc in stage_data["objects"]:
            kind = oc["kind"]
            if kind == "breakable":
                objects.append(BreakableObject(oc["x"], oc["y"], loot_type=oc.get("loot_type")))
            #elif kind == "barrel":
            #    objects.append(ExplosiveBarrel(oc["x"], oc["y"]))
        return objects
