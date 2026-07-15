GNEISS_ANIMATIONS = {
    "idle": {
        "file": "assets/enemies/gneiss_walk_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "walk": {
        "file": "assets/enemies/gneiss_walk_3x.png",
        "frames_count": 7,
        "frame_width": 256,
        "frame_height": 256,
    },
    "run": {
        "file": "assets/enemies/gneiss_run_3x.png",
        "frames_count": 6,
        "frame_width": 256,
        "frame_height": 256,
    },
    "attack": {
        "file": "assets/enemies/gneiss_attack_3x.png",
        "frames_count": 3,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (4,8,6)
    },
    "hit": {
        "file": "assets/enemies/gneiss_hit_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "grabbed": {
        "file": "assets/enemies/gneiss_grabbed_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "grab_kneed": {
        "file": "assets/enemies/gneiss_grab_kneed_3x.png",
        "frames_count": 1,
        "frame_width": 256,
        "frame_height": 256,
    },
    "dead": {
        "file": "assets/enemies/gneiss_dead_3x.png",
        "frames_count": 1,
        "frame_width": 384,
        "frame_height": 384,
        "frame_durations": (60,),
        "loop": False,
    },
}
# No dedicated "thrown" reaction art yet - reuse the flinch pose.
GNEISS_ANIMATIONS["thrown"] = GNEISS_ANIMATIONS["hit"]
