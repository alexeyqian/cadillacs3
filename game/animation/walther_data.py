WALTHER_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/walther_walk_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384
    },
    "walk": {
        "file": "assets/enemies/walther_walk_3x.png",
        "frames_count": 6,
        "frame_width": 384,
        "frame_height": 384
    },
    "attack": {
        "file": "assets/enemies/walther_attack_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (4,8,6)
    },
    "hit": {
        "file": "assets/enemies/walther_hit_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384
    },
    "dead": {
        "file": "assets/enemies/walther_dead_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
        "loop": False,
    },
}
# No dedicated grab-reaction art yet - reuse the flinch pose while held/kneed/thrown.
WALTHER_ANIMATIONS["grabbed"] = WALTHER_ANIMATIONS["hit"]
WALTHER_ANIMATIONS["grab_kneed"] = WALTHER_ANIMATIONS["hit"]
WALTHER_ANIMATIONS["thrown"] = WALTHER_ANIMATIONS["hit"]
