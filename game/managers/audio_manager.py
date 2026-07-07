from engine.event_bus import EventBus
from game.managers.asset_manager import AssetManager

# Attack name -> sound file. Keyed the same way AttackData.name doubles as
# the animation key, so adding a distinct sound per attack later is just
# adding an entry here - no combat code changes needed.
ATTACK_SOUNDS = {
    "attack": "assets/sounds/attack1.wav",
    "attack1": "assets/sounds/attack1.wav",
    "attack2": "assets/sounds/attack2.wav",
    "attack3": "assets/sounds/attack3.wav",
    "run_attack": "assets/sounds/run_attack.wav",
}

PLAYER_HIT_SOUND = "assets/sounds/player_hit.wav"
ENEMY_HIT_SOUND = "assets/sounds/enemy_hit.wav"
PLAYER_DEAD_SOUND = "assets/sounds/player_dead.wav"
ENEMY_DEAD_SOUND = "assets/sounds/enemy_dead.wav"


class AudioManager:
    """Plays sound effects in reaction to combat events on the EventBus,
    rather than being polled/called directly from combat code."""

    def __init__(self):
        EventBus.subscribe("attack_started", self.on_attack_started)
        EventBus.subscribe("hit_landed", self.on_hit_landed)
        EventBus.subscribe("entity_died", self.on_entity_died)

    def on_attack_started(self, attacker, attack_name):
        self._play(ATTACK_SOUNDS.get(attack_name))

    def on_hit_landed(self, target, amount, knockback):
        self._play(PLAYER_HIT_SOUND if "player" in target.tags else ENEMY_HIT_SOUND)

    def on_entity_died(self, entity):
        self._play(PLAYER_DEAD_SOUND if "player" in entity.tags else ENEMY_DEAD_SOUND)

    def _play(self, path):
        sound = AssetManager.load_sound(path)
        if sound:
            sound.play()