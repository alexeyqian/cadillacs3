######## system and sizes ########

FPS=60
SCREEN_WIDTH= 1920
SCREEN_HEIGHT= 1080
# total stage width, should around 3 screens
# Important: feet alignment matters most.anchor by feet, not by image center.
# Across idle, walk, attack, hit, etc., 
# the player’s feet should land on the same baseline. 
PLAYER_W=128 # static left/right facing width
PLAYER_H=256
# collision box is centered on bottom
# COLLISION UNIT == UNIT_LENGTH == PIXEL_PER_GRID == player shoulder width
PLAYER_COLLISION_W = 100
PLAYER_COLLISION_H = 50

# default for most of times
# some special movement might need special hurtbox
PLAYER_HURTBOX_W = PLAYER_COLLISION_W
PLAYER_HURTBOX_H = PLAYER_H
# Shorter while airborne (legs tucked up out of reach of low/sweep attacks).
# Anchored from the same top edge as PLAYER_HURTBOX_H, so only the leg
# region is excluded - see HurtboxComponent.get_rect().
PLAYER_HURTBOX_AIRBORNE_H = int(PLAYER_HURTBOX_H * 0.6)
PLAYER_HURTBOX_OFFSET_X=int(-1 * PLAYER_HURTBOX_W//2)
PLAYER_HURTBOX_OFFSET_Y=-1*PLAYER_H

PLAYER_HITBOX_W = int(PLAYER_W*1.3+30)
PLAYER_HITBOX_H = int(PLAYER_H*0.2)
PLAYER_HIT_BOX_OFFSET_X = int(PLAYER_W/2)
PLAYER_HIT_BOX_OFFSET_Y = int(-1*(PLAYER_HURTBOX_H + 50))

ENEMY_W=PLAYER_W
ENEMY_H=PLAYER_H
ENEMY_COLLISION_W = PLAYER_COLLISION_W
ENEMY_COLLISION_H = PLAYER_COLLISION_H
ENEMY_HURTBOX_W = ENEMY_COLLISION_W
ENEMY_HURTBOX_H = ENEMY_H - ENEMY_COLLISION_H
ENEMY_HURTBOX_OFFSET_X=int(-1 * ENEMY_HURTBOX_W//2)
ENEMY_HURTBOX_OFFSET_Y=-1*ENEMY_H

ENEMY_HITBOX_W = int(ENEMY_W*1)
ENEMY_HITBOX_H = int(ENEMY_H*0.2)
ENEMY_HITBOX_OFFSET_X = int(ENEMY_W/2)
ENEMY_HITBOX_OFFSET_Y = int(-1*(ENEMY_HURTBOX_H + 70))

######## debug ########
SHOW_DEBUG_INFO=True
# Dev only.
# None means start from the first stage normally.
# Can be a stage id, for example: "episode_1_stage_4_ruined_arena"
#"episode_1_stage_4_ruined_arena"
START_STAGE=None
# Skips loading/drawing every stage's real background art - each parallax
# layer (far/far_mid/near/ground/front) instead renders as its own striped
# color band, still scrolling at its real scroll_factor, so parallax speed
# and lane placement can be checked before any art exists (see
# game/world/background_layer.py, game/draw.py's lane overlay).
NO_IMAGES_FOR_STAGE=True
# Skips drawing every character's sprite frame - only their collision box
# (blue), hurtbox (green), and hitbox (red, while active) are drawn, same
# boxes SHOW_DEBUG_INFO already draws, just without needing a sprite frame
# underneath them (see CharacterRenderer.draw).
NO_IMAGES_FOR_CHARACTOR=False

######## health and score ########
PLAYER_LIVES=1 #3
PLAYER_MAX_HP=100
PLAYER_EXTRA_LIFE_SCORE_BASE=30000
PLAYER_EXTRA_LIFE_SCORE_STEP=30000
ENEMY_MAX_HP=int(PLAYER_MAX_HP*1)
ENEMY_SCORE_POINTS = 100
# Sprite blink cadence while the "dead" animation plays (frames per on/off half-cycle).
DEAD_FLASH_INTERVAL_FRAMES = 6

######## speed ########
# Pixels per second (movement is dt-scaled, not per-frame).
PLAYER_SPEED = 400
PLAYER_RUN_SPEED = int(PLAYER_SPEED * 3)
PLAYER_JUMP_POWER = 700
PLAYER_JUMP_AIR_MOVE_SPEED=PLAYER_SPEED*1.5 # horizontal air control after a normal jump
GRAVITY = 1500 # pixels per second
ENEMY_SPEED=int(PLAYER_SPEED*0.5)
ENEMY_RUN_SPEED=int(PLAYER_SPEED*0.9)
ENEMY_Y_SPEED=int(ENEMY_SPEED*0.5)
# Only meaningful for enemies with can_jump_attack=True (see enemy_config.py) -
# jump-attack hit timing is driven by the attack's own windup/active/recovery
# clock, not by physics (e.g. detecting landing), so these just need to be
# tuned to roughly match how long that clock runs.
ENEMY_JUMP_POWER = PLAYER_JUMP_POWER
ENEMY_JUMP_AIR_MOVE_SPEED = int(ENEMY_SPEED * 1.5)
ENEMY_RUN_CHASE_THRESHOLD=400  # pixels; enemy switches to run when farther than this
PROJECTILE_SPEED=PLAYER_SPEED*3
######## player attack ########
FIST_DAMAGE=20

ATTACK_1_DAMAGE=FIST_DAMAGE
ATTACK_1_WINDUP_DURATION=4
ATTACK_1_ACTIVE_DURATION=10
ATTACK_1_RECOVERY_DURATION=4
ATTACK_1_COOLDOWN=4
ATTACK_1_HIT_STUN_DURATION=20
ATTACK_1_KNOCKBACK_VELOCITY=100 # pixels per second (dt-scaled physics)
# Combo windows: how long after a hit finishes you can press attack again to
# continue the chain instead of it resetting to hit 1. Classic beat-em-ups
# (Streets of Rage, Final Fight) sit around 300-500ms - tight enough to need
# real input, generous enough not to feel like a fighting-game link. Widening
# slightly through the chain (hit1 -> hit2 -> hit3) is the common pattern,
# since later hits follow more committed animations and can afford more
# leniency. The finisher (hit 3) intentionally has no window - see
# DEFAULT_PLAYER_ATTACK_3_DATA - so it can't chain into anything.
ATTACK_1_COMBO_WINDOW=24 # 0.4s @ 60fps

ATTACK_2_DAMAGE=int(FIST_DAMAGE*1.2)
ATTACK_2_WINDUP_DURATION=4
ATTACK_2_ACTIVE_DURATION=10
ATTACK_2_RECOVERY_DURATION=4
ATTACK_2_COOLDOWN=4
ATTACK_2_HIT_STUN_DURATION=int(ATTACK_1_HIT_STUN_DURATION*1.2)
ATTACK_2_KNOCKBACK_VELOCITY=int(ATTACK_1_KNOCKBACK_VELOCITY*1.2)
ATTACK_2_COMBO_WINDOW=int(ATTACK_1_COMBO_WINDOW*1.2)

ATTACK_3_DAMAGE=int(FIST_DAMAGE*1.5)
ATTACK_3_WINDUP_DURATION=4
ATTACK_3_ACTIVE_DURATION=10
ATTACK_3_RECOVERY_DURATION=4
ATTACK_3_COOLDOWN=4
ATTACK_3_HIT_STUN_DURATION=int(ATTACK_1_HIT_STUN_DURATION*1.5)
ATTACK_3_KNOCKBACK_VELOCITY=int(ATTACK_1_COMBO_WINDOW*1.5)

# RUN ATTACK
# it's 0.25 seconds, should we use game frames as timer counter here?
RUN_TAP_WINDOW=0.25
RUN_ATTACK_REQUIRED_DISTANCE=100

RUN_ATTACK_DAMAGE=int(FIST_DAMAGE*2)
RUN_ATTACK_WINDUP_DURATION=4
RUN_ATTACK_ACTIVE_DURATION=10
RUN_ATTACK_RECOVERY_DURATION=4
RUN_ATTACK_COOLDOWN=10
RUN_ATTACK_HIT_STUN_DURATION=int(ATTACK_1_COMBO_WINDOW*2)
RUN_ATTACK_KNOCKBACK_VELOCITY=int(ATTACK_1_COMBO_WINDOW*2)

# todo: settings for jump attack
JUMP_ATTACK_DAMAGE=FIST_DAMAGE

# grab and throw
PLAYER_GRAB_RANGE=int(PLAYER_W * 0.9)
PLAYER_GRAB_KNEE_WINDUP_DURATION = 6
PLAYER_GRAB_KNEE_ACTIVE_DURATION = 4
PLAYER_GRAB_KNEE_RECOVERY_DURATION = 4
PLAYER_GRAB_KNEE_HIT_FRAME = PLAYER_GRAB_KNEE_WINDUP_DURATION
PLAYER_GRAB_KNEE_DAMAGE=int(FIST_DAMAGE*0.75)
# after this many knees land, the player auto-throws instead of waiting
# for another attack press - matches the classic "grab, knee x N, toss"
# beat-em-up combo rather than letting it continue indefinitely.
PLAYER_GRAB_KNEE_HIT_COUNT = 3
# pressing a direction (toward or away from the target) throws it that way
# immediately, once at least this many knees have landed - 0 means it's
# available the instant the grab starts, with no knees required. Only
# reachable before the last knee of PLAYER_GRAB_KNEE_HIT_COUNT, since the
# auto-throw already fires the instant that one lands.
PLAYER_GRAB_THROW_MIN_KNEES = 0
# If the player takes no action (knee or directional throw) within this
# long after grabbing (or after the last knee), the target breaks free
# instead of being held forever.
PLAYER_GRAB_HOLD_TIMEOUT = 90
THROWN_DAMAGE=int(FIST_DAMAGE*1.5)
# Big relative to normal hit knockback (ATTACK_1_KNOCKBACK_VELOCITY=100) on
# purpose - a throw should visibly launch the target several character-widths
# away, not just stagger it.
THROWN_KNOCKBACK_X = 1400
THROWN_KNOCKBACK_Z = -400
# How long the thrown target slides/lies in "hit" before it can act again,
# and how long the player holds the "throw" pose before returning to idle -
# both reuse the existing hit-stun/set_state("idle") timer pattern. Longer
# than a normal hit-stun so the full knockback has time to travel before
# the target can act (and be re-grabbed) again.
THROWN_STUN_DURATION = 40
PLAYER_THROW_POSE_DURATION = 16
# weapons
KNIFE_DAMAGE=int(FIST_DAMAGE*1.5)
BAT_DAMAGE=int(FIST_DAMAGE*2)
PISTOL_DAMAGE=int(FIST_DAMAGE*3)

######## enemy attack timing ########
ENEMY_DETECT_RANGE=int(SCREEN_WIDTH*0.50)
ENEMY_ATTACK_RANGE=130
ENEMY_ATTACK_LANE_RANGE=50

ENEMY_ATTACK_DAMAGE=int(ATTACK_1_DAMAGE*0.5)
ENEMY_ATTACK_WINDUP=10
ENEMY_ATTACK_ACTIVE=5
ENEMY_ATTACK_RECOVERY=20
ENEMY_ATTACK_COOLDOWN=20
ENEMY_ATTACK_HIT_STUN_DURATION=int(ATTACK_1_HIT_STUN_DURATION*0.5)
ENEMY_ATTACK_KNOCKBACK_VELOCITY=int(ATTACK_1_KNOCKBACK_VELOCITY*0.5)

# Which close-range attack an in-range enemy uses (normal punch / jump
# attack / run-charge attack, whichever it actually has) - re-rolled every
# ENEMY_ATTACK_CHOICE_DECISION_DURATION frames rather than every tick, same
# reasoning as ENEMY_RUN_DECISION_DURATION: commit to one choice for a
# beat instead of flickering between attacks. Weighted so the normal punch
# stays the common case and jump/run read as occasional variety, not the
# default.
ENEMY_ATTACK_CHOICE_DECISION_DURATION = 90
ENEMY_NORMAL_ATTACK_WEIGHT = 2
ENEMY_JUMP_ATTACK_WEIGHT = 1
ENEMY_RUN_ATTACK_WEIGHT = 1


# Only a small number of regular melee enemies 
# should enter ATTACK at the same time.
MAX_MELEE_ATTACKERS = 4
ENEMY_FLANK_OFFSET_X = 120
# avoid multiple enemies stack on the same lane.
# give flankers a small Z offset based on crowding.
ENEMY_FLANK_OFFSET_Z = 36
ENEMY_FLANK_DECISION_DURATION = 20
ENEMY_FLANK_Z_TOLERANCE = 18

# How often (frames) an enemy re-rolls whether it's running or walking while
# closing in on the player, and the odds it rolls "running" each time.
# Re-rolling on a timer (rather than every frame) keeps it from flickering
# between the two speeds/animations as it closes distance.
ENEMY_RUN_DECISION_DURATION = 90
ENEMY_RUN_CHANCE = 0.35

######## stage exit ########
# How long the exit's closed -> open transition takes once the player
# touches it (seconds). Applies whether the stage's exit is dressed up as
# a door, a window, or anything else.
STAGE_EXIT_OPEN_DURATION = 0.5
