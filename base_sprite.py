from pygame import *
from constants import win_width, win_height

#класс-родитель для других спрайтов
class GameSprite(sprite.Sprite):
    # конструктор класса
    def __init__(self, player_image, player_x, player_y, size_x, size_y, anime=None):
        # Вызываем конструктор класса (Sprite):
        sprite.Sprite.__init__(self)
        # каждый спрайт должен хранить свойство image - изображение
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        # анимация к спрайту
        self.anime = anime
        # размеры героя
        self.size_x = size_x
        self.size_y = size_y
        if self.anime:
             self.images = []
        # каждый спрайт должен хранить свойство rect - прямоугольник, в который он вписан
        # self.rect = self.image.get_rect()
        # self.rect.x = player_x
        # self.rect.y = player_y
        # self.rect.center = (player_x, player_y)
        # устанавливаем центр спрайта
        self.rect = self.image.get_rect()
        self.rect.center = (player_x, player_y)

    def reset(self, window):
        # window.blit(self.image, (self.rect.x, self.rect.y))
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


