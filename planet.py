import pygame
from pygame.sprite import Sprite
from PIL import Image, ImageSequence


class FinalGifSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, gif_path, scale=1.0, rotation_speed=1):
        super().__init__()
        self.frames = self._load_gif_frames(gif_path, scale)
        self.original_images = self.frames.copy()

        # Параметры анимации
        self.current_frame = 0
        self.animation_speed = 62  # ms per frame
        self.last_update = pygame.time.get_ticks()

        # Параметры вращения
        self.rotation_speed = rotation_speed
        self.angle = 0.0  # Используем float для плавности
        self.center = (x, y)

        # Инициализация
        self.image = self.frames[0]
        self.rect = self.image.get_rect(center=self.center)

    def _load_gif_frames(self, path, scale):
        frames = []
        gif = Image.open(path)

        # Для сохранения качества используем LANCZOS-интерполяцию
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            if scale != 1.0:
                new_size = (
                    int(frame.width * scale),
                    int(frame.height * scale)
                )
                frame = frame.resize(new_size, Image.Resampling.LANCZOS)

            pygame_frame = pygame.image.fromstring(
                frame.tobytes(),
                frame.size,
                "RGBA"
            ).convert_alpha()

            frames.append(pygame_frame)

        return frames

    def update(self, *args):
        # Плавное вращение с учетом delta time
        delta_time = pygame.time.get_ticks() - self.last_update
        self.angle += self.rotation_speed * (delta_time / 16.6667)
        self.angle %= 360

        # Обновление кадров
        if delta_time > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = pygame.time.get_ticks()

        # Создаем повернутое изображение
        original = self.original_images[self.current_frame]
        self.image = pygame.transform.rotozoom(
            original,
            self.angle,
            1  # Масштаб (1 = без изменения)
        )

        # Корректируем позицию
        self.rect = self.image.get_rect(center=self.center)