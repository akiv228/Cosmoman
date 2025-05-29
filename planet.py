import pygame
from pygame.sprite import Sprite
from PIL import Image, ImageSequence


class FinalGifSprite(Sprite):
    def __init__(self, x, y, gif_path, scale=1.0, rotation_speed=36):
        super().__init__()
        self.frames = self._load_gif_frames(gif_path, scale)
        self.original_images = self.frames.copy()

        # (10 секунд на 60 кадров)
        self.total_frames = 60
        self.frame_delay = 0.167  # 167 ms per frame
        self.current_frame = 0
        self.last_frame_update = pygame.time.get_ticks()

        # (36 градусов/сек для полного оборота за 10 сек)
        self.rotation_speed = rotation_speed  # градусов за кадр
        self.angle = 0.0
        self.last_rotation_update = pygame.time.get_ticks()
        self.center = (x, y)

        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=self.center)

    def _load_gif_frames(self, path, scale):
        frames = []
        gif = Image.open(path)

        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            if scale != 1.0:
                new_size = (int(frame.width * scale), int(frame.height * scale))
                frame = frame.resize(new_size, Image.Resampling.LANCZOS)

            pygame_frame = pygame.image.fromstring(
                frame.tobytes(),
                frame.size,
                "RGBA"
            ).convert_alpha()
            frames.append(pygame_frame)
        return frames

    def update(self, *args):
        now = pygame.time.get_ticks()

        # обновление анимации (строго по таймингу кадров)
        if now - self.last_frame_update >= self.frame_delay * 1000:
            self.current_frame = (self.current_frame + 1) % self.total_frames
            self.last_frame_update = now

        # плавное вращение с фиксированной скоростью
        time_since_last_rotation = now - self.last_rotation_update
        self.angle += self.rotation_speed * (time_since_last_rotation / 1000)
        self.angle %= 360
        self.last_rotation_update = now

        # применение трансформаций
        original = self.original_images[self.current_frame]
        self.image = pygame.transform.rotozoom(original, self.angle, 1)
        self.rect = self.image.get_rect(center=self.center)