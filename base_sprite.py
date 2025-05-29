from pygame import *
from config import win_width, win_height

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, anime=None):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.anime = anime
        self.size_x = size_x
        self.size_y = size_y
        if self.anime:
             self.images = []
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# from PIL import Image, ImageSequence
#
# class GameSprite(pg.sprite.Sprite):
#     def __init__(self, image_path, x, y, width, height, anime=False):
#         super().__init__()
#         self.image_path = image_path
#         if image_path.endswith('.gif'):
#             self.frames = self._load_gif_frames(image_path, width, height)
#             self.is_animated = True
#             self.current_frame = 0
#             self.last_update = pg.time.get_ticks()
#             self.frame_rate = 100  # миллисекунды на кадр
#             self.image = self.frames[0]
#         else:
#             self.image = pg.image.load(image_path).convert_alpha()
#             self.image = pg.transform.scale(self.image, (width, height))
#             self.is_animated = False
#         self.rect = self.image.get_rect(center=(x, y))
#
#     def _load_gif_frames(self, path, width, height):
#         frames = []
#         gif = Image.open(path)
#         for frame in ImageSequence.Iterator(gif):
#             frame = frame.convert("RGBA")
#             frame = frame.resize((width, height), Image.Resampling.LANCZOS)
#             pygame_frame = pg.image.fromstring(
#                 frame.tobytes(), frame.size, "RGBA"
#             ).convert_alpha()
#             frames.append(pygame_frame)
#         return frames
#
#     def update(self):
#         if self.is_animated:
#             now = pg.time.get_ticks()
#             if now - self.last_update > self.frame_rate:
#                 self.current_frame = (self.current_frame + 1) % len(self.frames)
#                 self.image = self.frames[self.current_frame]
#                 self.last_update = now
# #


# class GameSprite(pg.sprite.Sprite):
#     def __init__(self, image_path, x, y, width, height, rotated):
#         super().__init__()
#         image = pg.image.load(image_path).convert_alpha()
#         self.image = pg.transform.scale(image, (width, height))
#         if rotated:
#             self.image = pg.transform.rotate(self.image, 90)
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#     def reset(self, window):
#         window.blit(self.image, (self.rect.x, self.rect.y))


