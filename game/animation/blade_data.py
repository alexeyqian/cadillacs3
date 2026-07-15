BLADE_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/blade_walk_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "walk": {
        "file": "assets/enemies/blade_walk_3x.png",
        "frames_count": 5,
        "frame_width": 256,
        "frame_height": 256,
    },
    "attack": {
        "file": "assets/enemies/blade_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (4,8,6)
    },
    # He only ever jumps to attack (see enemy_config.py's jump_attack,
    # name="jump") - one clip covers the whole leap, no separate
    # non-attacking "jump_attack" state to distinguish it from.
    "jump": {
        "file": "assets/enemies/blade_jump_attack_3x.png",
        "frames_count": 4,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (2,2,8,6)
    },
    "hit": {
        "file": "assets/enemies/blade_hit_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "dead": {
        "file": "assets/enemies/blade_dead_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
        "loop": False,
    },
}
# No dedicated grab-reaction art yet - reuse the flinch pose while held/kneed/thrown.
BLADE_ANIMATIONS["grabbed"] = BLADE_ANIMATIONS["hit"]
BLADE_ANIMATIONS["grab_kneed"] = BLADE_ANIMATIONS["hit"]
BLADE_ANIMATIONS["thrown"] = BLADE_ANIMATIONS["hit"]
# No dedicated charge-attack art yet - reuse the standing punch pose.
BLADE_ANIMATIONS["run_attack"] = BLADE_ANIMATIONS["attack"]
