
class CharacterState:
    IDLE = "IDLE"
    WALK = "WALK"
    RUN = "RUN"
    JUMP = "JUMP"
    ATTACK = "ATTACK"
    RUN_ATTACK = "RUN_ATTACK"
    JUMP_ATTACK = "JUMP_ATTACK"

    HIT = "HIT"
    # RECOIL means clash bounce/no damage
    RECOIL = "RECOIL"
    DEAD = "DEAD"

    KNOCKDOWN = "KNOCKDOWN"
    GETUP = "GETUP"

class PlayerState(CharacterState):
    ATTACK2 = "ATTACK2"
    ATTACK3 = "ATTACK3"

    GRAB = "GRAB"
    GRAB_KNEE = "GRAB_KNEE"
    THROW = "THROW"

class EnemyState(CharacterState):
    PATROL = "PATROL" # ai decisions
    CHASE = "CHASE"
    GRABBED = "GRABBED"
    THROWN = "THROWN"
