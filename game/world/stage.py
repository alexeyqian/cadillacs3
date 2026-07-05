from game.world.lane import Lane
from game.world.wave import SpawnInstruction, Wave
from game.world.background import Background
from game.entities.breakable_object import BreakableObject
# from game.entities.explosive_barrel import ExplosiveBarrel
from game.entities.weapon import Weapon

class Stage:
    def __init__(self, camera, player, stage_data):
        self.camera = camera
        self.player = player
        self.enemies = []
        self._load_from_data(stage_data)

    def get_all_entities(self):
        return [self.player]
        # todo: add others: weapons, projectiles, sparks, objects etc
        #return [self.player] + self.enemies # plus others

    def _load_from_data(self, stage_data):
        self.stage_id = stage_data["id"]
        self.stage_name = stage_data["name"]
        self.world_width = stage_data["world_width"]
        self.world_height = stage_data["world_height"]
        self.exit_rect = stage_data["exit_rect"]
        self.completion = stage_data["completion"]

        self.lane_top = stage_data["lane_top"]
        self.lane_bottom = stage_data["lane_bottom"]
        self.lane_system = Lane(self.lane_top, self.lane_bottom)

        self.waves = self._build_waves(stage_data["waves"])

        far = stage_data.get("background_far", stage_data["background"])
        mid = stage_data.get("background_mid", stage_data["background"])
        self.background = Background(
            far,
            mid_file=mid,
            front_file=stage_data.get("background_front"),
        )

    def _build_waves(self, wave_configs):
        waves = []
        for wave_config in wave_configs:
            spawn_instructions = []
            for spawn_config in wave_config["spawns"]:
                count = spawn_config.get("count", 1)
                for _ in range(count):
                    spawn_instructions.append(SpawnInstruction(
                        enemy_type=spawn_config["enemy_type"],
                        side=spawn_config.get("side", "right"),
                        capability_overrides=spawn_config.get("capability_overrides"),
                    ))

            waves.append(Wave(
                stage=self,
                trigger_x=wave_config["trigger_x"],
                spawn_instructions=spawn_instructions,
                max_active=wave_config.get("max_active", 4),
            ))
        return waves
    
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
