from dataclasses import dataclass
from typing import Optional
from game.settings import *
from game.entities.attack_data import AttackData, DEFAULT_ENEMY_ATTACK_DATA, make_attack_data


GNEISS_SCALER=1.2
BLACK_ELMER_SCALER=1.5
WALTHER_SCALER=3
DEFAULT_ENEMY_TYPE = "ferris"

@dataclass(frozen=True)
class EnemyConfig:
    enemy_id: str
    display_name: str = "Enemy"
    archetype: str = "basic_melee"

    collision_box_w: int = ENEMY_COLLISION_W
    collision_box_h: int = ENEMY_COLLISION_H

    hurt_box_w: int = ENEMY_HURTBOX_W
    hurt_box_h: int = ENEMY_HURTBOX_H
    hurt_box_offset_x: int = ENEMY_HURTBOX_OFFSET_X
    hurt_box_offset_y: int = ENEMY_HURTBOX_OFFSET_Y

    max_hp: int = ENEMY_MAX_HP
    speed: float = ENEMY_SPEED
    can_run: bool = False
    run_speed: float = ENEMY_RUN_SPEED
    can_run_attack: bool = False
    run_attack: Optional[AttackData] = None
    can_jump: bool = False
    can_jump_attack: bool = False
    jump_attack: Optional[AttackData] = None
    jump_power: float = ENEMY_JUMP_POWER
    jump_air_move_speed: float = ENEMY_JUMP_AIR_MOVE_SPEED

    attack: AttackData = DEFAULT_ENEMY_ATTACK_DATA
    score_points: int = ENEMY_SCORE_POINTS
    sprite_scale: int  = 1

    # enemy specific
    patrol_distance:int = ENEMY_DETECT_RANGE
    detect_range: float = ENEMY_DETECT_RANGE
    attack_range:int = ENEMY_ATTACK_RANGE
    attack_lane_range:int = ENEMY_ATTACK_LANE_RANGE

    # give heavy enemies poise, so weak punches still deal damage
    # but do not always interrupt them.
    flinch_damage_threshold: int = 0
    knockdown_damage_threshold: int = 40

    max_melee_attackers:int = 2 # move to stage config?
    melee_attack_slot_limit: Optional[int] = None
# Each enemy archetype has a readable combat rhythm:
# Ferris   = basic pressure, fair but less passive.
# Gneiss   = fast striker, quicker startup and shorter cooldown.
# Elmer    = heavy bruiser, bigger reach and attack poise.
ENEMY_CONFIGS = {
    "ferris": EnemyConfig(
        enemy_id="ferris",
        display_name="Ferris",
        can_run=True,

        attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            hitbox_offset_x=96, hitbox_offset_y=-200, hitbox_w=96, hitbox_h=50,
        ),
    ),

    "gneiss": EnemyConfig(
        enemy_id="gneiss",
        display_name="Gneiss",
        sprite_scale=1,
        max_hp=int(ENEMY_MAX_HP * GNEISS_SCALER),
        speed=int(ENEMY_SPEED),
        can_run=True,

        attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            damage=int(ENEMY_ATTACK_DAMAGE * GNEISS_SCALER),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * 0.8),
            windup=ENEMY_ATTACK_WINDUP,
            active=ENEMY_ATTACK_ACTIVE,
            recovery=ENEMY_ATTACK_RECOVERY,
            hitbox_offset_x=96, hitbox_offset_y=-200, hitbox_w=96, hitbox_h=50,
        ),
        score_points=int(ENEMY_SCORE_POINTS*GNEISS_SCALER),
    ),

    "blade": EnemyConfig(
        enemy_id="blade",
        display_name="Blade",
        max_hp=int(ENEMY_MAX_HP * 1.5),
        speed=int(ENEMY_SPEED),
        can_run=True,
        can_jump=True,
        can_jump_attack=True,
        can_run_attack=True,

        attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            damage=int(ENEMY_ATTACK_DAMAGE * 1.5),
            cooldown=int(ENEMY_ATTACK_COOLDOWN * 0.8),
            windup=ENEMY_ATTACK_WINDUP,
            active=ENEMY_ATTACK_ACTIVE,
            recovery=ENEMY_ATTACK_RECOVERY,
            hitbox_offset_x=24, hitbox_offset_y=-240, hitbox_w=170, hitbox_h=100,
        ),
        # Charging slash - keep_moving=True closes the last stretch of
        # distance through the hit, matching a running attack's momentum.
        run_attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            name="run_attack",
            keep_moving=True,
            damage=int(ENEMY_ATTACK_DAMAGE * 1.5),
            windup=8, active=8, recovery=10,
            hitbox_offset_x=30, hitbox_offset_y=-230, hitbox_w=160, hitbox_h=100,
        ),
        # Agile knife stab, mid-air - hitbox timed to land during the jump's
        # ascent/apex (jump_power/GRAVITY gives ~56f of hang time), not on
        # landing. name="jump" (not a separate "jump_attack") - he only ever
        # jumps to attack, so there's no distinct non-attacking jump state/
        # animation to tell apart from it.
        jump_attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            name="jump",
            keep_moving=True,
            damage=int(ENEMY_ATTACK_DAMAGE * 1.5),
            windup=12, active=8, recovery=12,
            hitbox_offset_x=64, hitbox_offset_y=-354, hitbox_w=85, hitbox_h=100,
        ),
        score_points=int(ENEMY_SCORE_POINTS*1.5),
    ),

    "black_elmer": EnemyConfig(
        enemy_id="black_elmer",
        display_name="Black Elmer",
        archetype="heavy",

        max_hp=ENEMY_MAX_HP * 2,
        speed=int(ENEMY_SPEED * 0.7),
        # Doesn't jog while closing distance (heavy, always walks) - but
        # can_run_attack is independent of that, see _roll_close_attack:
        # a deliberate bull-rush special move, not tied to his everyday
        # movement speed.
        can_run=False,
        run_speed=int(ENEMY_RUN_SPEED * 0.9),
        can_run_attack=True,
        can_jump=True,
        can_jump_attack=True,
        # Doesn't leap high - a heavy hop before dropping his full weight,
        # not an agile jump (contrast blade's ENEMY_JUMP_POWER default).
        jump_power=int(ENEMY_JUMP_POWER * 0.85),

        attack_range=int(ENEMY_ATTACK_RANGE * BLACK_ELMER_SCALER),
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * BLACK_ELMER_SCALER),
        attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            cooldown=int(ENEMY_ATTACK_COOLDOWN * BLACK_ELMER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*BLACK_ELMER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*BLACK_ELMER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*BLACK_ELMER_SCALER),
            lane_reach=1,
            hitbox_offset_x=92, hitbox_offset_y=-185, hitbox_w=100, hitbox_h=100,
        ),
        # Shoulder charge - keep_moving=True lets him plow the last bit of
        # distance into the hit.
        run_attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            name="run_attack",
            keep_moving=True,
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            windup=15, active=15, recovery=20,
            hitbox_offset_x=50, hitbox_offset_y=-180, hitbox_w=150, hitbox_h=110,
        ),
        # Body-slam: sits his full weight down on whoever's underneath -
        # wide, centered, low AoE box rather than a forward-reaching poke,
        # active for a generous window since the impact itself (not precise
        # timing) is the read. HitboxComponent.get_rect() anchors offset_x
        # to extend forward from the facing edge, not centered on the body -
        # offset_x=-width/2 is what makes it straddle him symmetrically
        # regardless of which way he's facing when he lands. He doesn't
        # close distance mid-jump (move_x stays 0 while attacking), so the
        # box's half-width has to reach at least as far as attack_range
        # (~195px here), or he can trigger the attack from a spot the slam
        # can't actually cover. name="jump" (not "jump_attack") - he only
        # ever jumps to slam, so there's no separate non-attacking jump
        # animation to distinguish it from.
        jump_attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            name="jump",
            keep_moving=True,
            damage=ENEMY_ATTACK_DAMAGE * BLACK_ELMER_SCALER,
            windup=20, active=20, recovery=20,
            hitbox_offset_x=-220, hitbox_offset_y=-140, hitbox_w=440, hitbox_h=140,
        ),
        # todo: simplify it
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 4,

        score_points=int(ENEMY_SCORE_POINTS * BLACK_ELMER_SCALER),
    ),

    "walther": EnemyConfig(
        enemy_id="walther",
        display_name="Walther",
        archetype="heavy",

        max_hp=ENEMY_MAX_HP * 4,
        speed=int(ENEMY_SPEED * 0.7),
        # attack_range gates when the AI decides it's close enough to swing
        # (see Enemy.update_intention's in_range check) - it has to stay
        # within what the punch's hitbox can actually reach (offset_x=64 +
        # hitbox_w=128 = 192px), or he throws punches from a distance that
        # can never connect. Scaling it by WALTHER_SCALER (*3, same as his
        # damage/timing) blew past that - 390 vs a 192px reach - so it's a
        # fixed value here instead, comfortably under the hitbox's reach.
        attack_range=170,
        attack_lane_range=int(ENEMY_ATTACK_LANE_RANGE * WALTHER_SCALER),
        attack=make_attack_data(
            base=DEFAULT_ENEMY_ATTACK_DATA,
            damage=ENEMY_ATTACK_DAMAGE * WALTHER_SCALER,
            cooldown=int(ENEMY_ATTACK_COOLDOWN * WALTHER_SCALER),
            windup=int(ENEMY_ATTACK_WINDUP*WALTHER_SCALER),
            active=int(ENEMY_ATTACK_ACTIVE*WALTHER_SCALER),
            recovery=int(ENEMY_ATTACK_RECOVERY*WALTHER_SCALER),
            lane_reach=1,
            hitbox_offset_x=64, hitbox_offset_y=-264, hitbox_w=128, hitbox_h=100,
        ),
        # So Black Elmer only flinches from the heavy punch
        # light punch hits still reduce HP, but he can keep acting.
        flinch_damage_threshold=FIST_DAMAGE + 100, # means no flinch

        score_points=int(ENEMY_SCORE_POINTS * WALTHER_SCALER),
    ),

}

def get_enemy_config(enemy_type):
    return ENEMY_CONFIGS.get(enemy_type, ENEMY_CONFIGS[DEFAULT_ENEMY_TYPE])
