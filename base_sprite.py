from pygame import *



class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y, anime=None):
        sprite.Sprite.__init__(self)
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

