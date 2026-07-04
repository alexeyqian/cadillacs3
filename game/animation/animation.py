from dataclasses import dataclass
import pygame

DEFAULT_ANIM_DURATION = 5


def get_bottom_center_offset(frame_size):
    frame_w, frame_h = frame_size
    return (-frame_w / 2, -frame_h)


def build_default_frame_configs(frame_count, frame_size, offset=None):
    frame_w, frame_h = frame_size
    if offset is None:
        offset = get_bottom_center_offset(frame_size)

    return [
        {
            "frame_rect": (frame_index * frame_w, 0, frame_w, frame_h),
            "offset": offset,
        }
        for frame_index in range(frame_count)
    ]


def get_configured_frame_size(config):
    if "frame_width" in config and "frame_height" in config:
        return (config["frame_width"], config["frame_height"])

    return config["default_frame_size"]


def get_frame_configs(config):
    if "frame_width" in config and "frame_height" in config:
        return build_default_frame_configs(
            config["frames_count"],
            get_configured_frame_size(config),
        )

    frame_configs = config.get("frames")
    if frame_configs is not None:
        return frame_configs

    return build_default_frame_configs(
        config["frames_count"],
        get_configured_frame_size(config),
        config.get("default_offset"),
    )


def get_frame_durations(config, frame_count):
    # Priority 1: explicit per-frame durations
    frame_durations = config.get("frame_durations")
    if frame_durations is not None:
        if len(frame_durations) != frame_count:
            raise ValueError(
                f"Animation has {frame_count} frames but "
                f"{len(frame_durations)} frame durations"
            )
        return [max(1, int(d)) for d in frame_durations]

    # Priority 2: total_duration spread equally across frames
    total = config.get("total_duration")
    if total is not None:
        ticks = max(1, total // frame_count)
        return [ticks] * frame_count

    # Priority 3: global default
    return [DEFAULT_ANIM_DURATION] * frame_count



        
def load_frame_animation(animation_data, animation_key):
    config = animation_data.get(animation_key)
    if not config:
        raise ValueError(f"Missing frame animation data: {animation_key}")
    
    sheet = pygame.image.load(config["file"]).convert_alpha()
    frames = []
    frame_configs = get_frame_configs(config)

    for frame_config in frame_configs:
        frame_x, frame_y, frame_w, frame_h = frame_config["frame_rect"]
        image = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
        image.blit(sheet, (0,0),(frame_x, frame_y, frame_w, frame_h))

        frames.append(FrameData(
            image=image,
            offset=get_bottom_center_offset((frame_w, frame_h)),
            scale=frame_config.get("scale", config.get("scale")),
            hitbox=frame_config.get("hitbox", config.get("hitbox")),
        ))
    if not frames:
        raise ValueError(f"No frames loaded for animation: {animation_key}")
    
    return frames
