from game.level.lane import Lane
from game.level.wave import SpawnInstruction, Wave
from game.level.background import Background

class Level:
    def __init__(self, stage_data):
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
                trigger_x=wave_config["trigger_x"],
                spawn_instructions=spawn_instructions,
                max_active=wave_config.get("max_active", 4),
            ))
        return waves
