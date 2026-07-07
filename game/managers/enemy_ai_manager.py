from game.settings import (
    FPS,
    MAX_MELEE_ATTACKERS,
    ENEMY_FLANK_OFFSET_X,
    ENEMY_FLANK_OFFSET_Z,
    ENEMY_FLANK_DECISION_DURATION,
)

# Which lane row (relative to the player) each flank slot holds, so waiting
# enemies spread across a few lanes instead of queueing up in a single file.
_LANE_PATTERN = (0, 1, -1, 2, -2)


class EnemyAIManager:
    """Coordinates enemy AI each frame so a crowd doesn't instantly mob the
    player: only the closest MAX_MELEE_ATTACKERS enemies get an "attack
    slot" (may close in and attack); everyone else holds a flanking position
    around the player instead of stacking directly on top of them or of
    each other."""

    def __init__(self):
        self._flank_slots = {}
        self._next_flank_slot = 0
        self._decision_timer = 0.0

    def resolve(self, dt, player, enemies):
        alive_enemies = [e for e in enemies if e.alive]

        for enemy in alive_enemies:
            enemy.flank_target = self._flank_target(enemy, player)

        # Re-ranking "who's closest" every single frame would let attack
        # slots flicker between enemies hovering near the same distance.
        # Only re-decide who holds a slot every ENEMY_FLANK_DECISION_DURATION.
        self._decision_timer -= dt
        if self._decision_timer > 0:
            return
        self._decision_timer = ENEMY_FLANK_DECISION_DURATION / FPS

        alive_enemies.sort(key=lambda e: self._distance_to_player(e, player))
        attacker_ids = {id(e) for e in alive_enemies[:MAX_MELEE_ATTACKERS]}
        for enemy in alive_enemies:
            enemy.has_attack_slot = id(enemy) in attacker_ids

    def _distance_to_player(self, enemy, player):
        dx = player.x - enemy.x
        dz = player.z - enemy.z
        return (dx * dx + dz * dz) ** 0.5

    def _flank_target(self, enemy, player):
        slot = self._flank_slots.get(id(enemy))
        if slot is None:
            slot = self._next_flank_slot
            self._next_flank_slot += 1
            self._flank_slots[id(enemy)] = slot

        # Stay on whichever side of the player the enemy is already on,
        # just staggered further out by rank - sending it to a target on the
        # opposite side would route it straight through the player's (and
        # other enemies') collision boxes, since there's no lane-routing.
        side = 1 if enemy.x >= player.x else -1
        rank = slot // 2 + 1
        x_offset = side * ENEMY_FLANK_OFFSET_X * rank
        z_offset = _LANE_PATTERN[slot % len(_LANE_PATTERN)] * ENEMY_FLANK_OFFSET_Z

        return (player.x + x_offset, player.z + z_offset)
