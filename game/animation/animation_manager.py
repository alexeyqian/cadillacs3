from dataclasses import dataclass
import pygame

@dataclass
class AnimationFrame: # single frame
    image: pygame.Surface
    offset: tuple
    hitbox: tuple = None

class Animation: # multiple frames
    def __init__(self, name, frames, frame_durations=None, loop=True):
        self.name = name
        self.frames = frames # multiple AnimationFrame
        self.default_frame_duration = 8
        self.frame_durations = frame_durations
        self.loop = loop

        self.current_frame = 0
        self.timer = 0
        self.finished = False

    def update(self):
        self.timer += 1
        if self.timer < self._get_current_frame_duration():
            return

        self.timer = 0
        self.current_frame += 1

        if self.current_frame < len(self.frames):
            return

        if self.loop:
            self.current_frame = 0
        else:
            self.current_frame = len(self.frames) - 1
            self.finished = True

    def get_current_frame(self)-> AnimationFrame:
        return self.frames[self.current_frame]

    def _get_current_frame_duration(self):
        if self.frame_durations != None:
            return self.frame_durations[self.current_frame]

        return self.default_frame_duration

    def _get_total_duration(self):
        if self.frame_durations != None:
            return sum(self.frame_durations)

        return len(self.frames) * self.default_frame_duration

    def reset(self):
        self.current_frame = 0
        self.timer = 0
        self.finished = False

class AnimationManager:
    def __init__(self, animation_data: dict):
        self.animation_data = animation_data

        self.animations = self._load_animations(animation_data)
        self.current_name: str = None
        self.current_animation: Animation = None
        
    def _load_animations(self, animation_data):
        animations = {}
        for name, config in animation_data.items():
            sheet = pygame.image.load(config["file"]).convert_alpha()
            frames = []
            frame_count = config["frames_count"]
            frame_width = config.get("frame_width", 384)
            frame_height = config.get("frame_height", 384)
            offset = (-frame_width / 2, -frame_height)

            for frame_index in range(frame_count):
                frame_rect = (frame_index * frame_width, 0, frame_width, frame_height)
                frame_x, frame_y, frame_w, frame_h = frame_rect
                image = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA)
                image.blit(sheet, (0,0),(frame_x, frame_y, frame_w, frame_h))

                frames.append(AnimationFrame(
                    image=image,
                    offset=offset,
                    hitbox=config.get("hitbox"),
                ))
            animations[name] = Animation(
                name,
                frames,
                frame_durations=config.get("frame_durations"),
                loop=config.get("loop", True),
            )

        return animations

    def get_current_frame(self):
        return self.current_animation.get_current_frame()

    def is_finished(self):
        return self.current_animation is not None and self.current_animation.finished

    def update(self, name):
        if name != self.current_name:
            next_animation = self.animations.get(name)
            if next_animation is None:
                return

            self.current_name = name
            self.current_animation = next_animation
            self.current_animation.reset()

        self.current_animation.update()
