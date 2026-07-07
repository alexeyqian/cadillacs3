import json
import os

from game.components.health_component import HealthComponent

SAVE_FILE_PATH = "savegame.json"


class SaveManager:
    """Saves/restores just enough to resume a run: which stage the player
    was on, plus their score/lives/health/position on it."""

    @staticmethod
    def has_save():
        return os.path.exists(SAVE_FILE_PATH)

    @staticmethod
    def save(player, stage):
        data = {
            "stage_id": stage.stage_id,
            "player_x": player.x,
            "player_z": player.z,
            "score": player.score,
            "lives": player.lives,
            "health": player.get_component(HealthComponent).health,
        }
        with open(SAVE_FILE_PATH, "w") as save_file:
            json.dump(data, save_file)

    @staticmethod
    def load(player, stage_manager):
        """Loads the saved stage and restores the player onto it. Returns
        the loaded Stage, or None if there's no save file to load."""
        if not SaveManager.has_save():
            return None

        with open(SAVE_FILE_PATH) as save_file:
            data = json.load(save_file)

        # Loading a stage resets the player to that stage's default spawn
        # point, so the saved position/stats are applied after.
        stage = stage_manager.load_stage_by_id(data["stage_id"])
        player.x = data["player_x"]
        player.z = data["player_z"]
        player.score = data["score"]
        player.lives = data["lives"]
        player.get_component(HealthComponent).health = data["health"]
        return stage
