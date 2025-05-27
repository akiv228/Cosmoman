import pygame
from pygame.sprite import Sprite
from PIL import Image, ImageSequence


class FinalGifSprite(Sprite):  # Наследуемся от Sprite
    def __init__(self, x, y, gif_path, scale=1.0, rotation_speed=1):
        super().__init__()  # Важно вызвать конструктор родителя

        # Загрузка кадров
        self.frames = self._load_gif_frames(gif_path, scale)
        self.current_frame = 0
        self.last_update = pygame.time.get_ticks()

        # Настройки анимации
        self.animation_speed = 62  # ms per frame
        self.rotation_speed = rotation_speed
        self.angle = 0

        # Инициализация изображения и rect (обязательные атрибуты)
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(center=(x, y))

        # Сохраняем оригинальные изображения для вращения
        self.original_images = self.frames.copy()

    def _load_gif_frames(self, path, scale):
        # Тот же код загрузки, что и ранее
        frames = []
        gif = Image.open(path)
        for frame in ImageSequence.Iterator(gif):
            frame = frame.convert("RGBA")
            pygame_frame = pygame.image.fromstring(
                frame.tobytes(), frame.size, "RGBA"
            ).convert_alpha()
            if scale != 1.0:
                new_size = (int(pygame_frame.get_width() * scale),
                            int(pygame_frame.get_height() * scale))
                pygame_frame = pygame.transform.scale(pygame_frame, new_size)
            frames.append(pygame_frame)
        return frames

    def update(self, *args, **kwargs):  # Метод update обязателен
        # Обновление анимации
        now = pygame.time.get_ticks()
        if now - self.last_update > self.animation_speed:
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.last_update = now

        # Обновление вращения
        self.angle = (self.angle + self.rotation_speed) % 360
        original = self.original_images[self.current_frame]
        self.image = pygame.transform.rotate(original, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)