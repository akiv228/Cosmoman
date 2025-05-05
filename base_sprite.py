from pygame import *
from config import win_width, win_height

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, anime=None):
        super().__init__()
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


