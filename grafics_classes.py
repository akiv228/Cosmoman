import pygame as pg
from pygame import Surface
from constants import *
from base_sprite import GameSprite
from grafics import Starfield, Star2

class Backgrounds:
    def __init__(self, image_path, w, h, x, y):
        self.image = pg.transform.scale(pg.image.load(image_path), (w, h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def reset(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Menu(GameSprite):
    def __init__(self, image_path, x, y, width, height):
        super().__init__(image_path, x, y, width, height, False)

    def collidepoint(self, x, y):
        return self.rect.collidepoint(x, y)

class Label:
    def __init__(self, x, y, width, height, color):
        self.rect = pg.Rect(x, y, width, height)
        self.color = color
        self.font = None
        self.text = None

    def set_text(self, text, size, text_color):
        self.font = pg.font.Font(None, size)
        self.text = self.font.render(text, True, text_color)

    def draw(self, window, shift_x = 0, shift_y = 0):
        if self.text:
            window.blit(self.text, (self.rect.x + shift_x, self.rect.y + shift_y))


class Fon:
    def __init__(self, w, h, stars_count):
        self.starfield = Starfield(w, h, stars_count)

    def update(self, window):
        window.blit(self.starfield.alpha_surface, (0, 0))
        self.starfield.run()

class Fon2():
    def __init__(self, w, h, stars_count=3000) -> None:
        self.w = w
        self.h = h
        self.x = -1000
        self.y = -200
        self.image = Surface((w, h))
        self.rect = self.image.get_rect()
        self.stars_count = stars_count
        self.stars = []
        self.fill_stars()

    # заполнение звёздам
    def fill_stars(self):
        for i in range(self.stars_count):
            self.stars.append(Star2(self.w, self.h))

    def update(self, scr):
        self.image.fill(BLACK)
        for star in self.stars:
            star.update()
            self.image.blit(star.image, (star.rect.x, star.rect.y))
        scr.blit(self.image, (self.x, self.y))


class InputBox(pg.sprite.Sprite):
    def __init__(self, x, y, w, h, placeholder='', inactive_color=(200, 200, 200), active_color=(255, 255, 255), is_password=False):
        super().__init__()
        self.rect = pg.Rect(x, y, w, h)
        self.color = inactive_color
        self.inactive_color = inactive_color
        self.active_color = active_color
        self.placeholder = placeholder
        self.text = ''
        self.text_color = (255, 255, 255)
        self.font = pg.font.Font(None, 32)
        self.active = False
        self.is_password = is_password
        self.image = pg.Surface((w, h), pg.SRCALPHA)
        
    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = self.active_color if self.active else self.inactive_color
        
        if event.type == pg.KEYDOWN and self.active:
            if event.key == pg.K_RETURN:
                return True
            elif event.key == pg.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                self.text += event.unicode
    
    def update(self):
        # Обновляем изображение для отрисовки
        self.image.fill((0, 0, 0, 0))  # Прозрачный фон
        pg.draw.rect(self.image, self.color, (0, 0, self.rect.w, self.rect.h), 2)
        
        if not self.text and not self.active:
            text_surface = self.font.render(self.placeholder, True, (150, 150, 150))
        else:
            display_text = '*' * len(self.text) if self.is_password else self.text
            text_surface = self.font.render(display_text, True, self.text_color)
        
        self.image.blit(text_surface, (5, 5))
    
    def draw(self, surface):
        surface.blit(self.image, self.rect)

#
# import pygame; import random; import math
# from pygame import SRCALPHA; from constants import *
#
#
# # Screensaver & Label
# class Screensaver:
#     def __init__(self,x,y,w,h,color): self.rect=pygame.Rect(x,y,w,h); self.color=color
#     def fill(self,surf): pygame.draw.rect(surf,self.color,self.rect)
# class Label(Screensaver):
#     def __init__(self,x,y,w,h,text,size,color): super().__init__(x,y,w,h,None); self.font=pygame.font.SysFont('serif',size); self.image=self.font.render(text,True,color)
#     def draw(self,surf): self.fill(surf); surf.blit(self.image,(self.rect.x,self.rect.y))
# # Menu button
# class Menu(Screensaver):
#     def __init__(self,image,x,y,w,h): super().__init__(x,y,w,h,None); self.image=pygame.transform.scale(pygame.image.load(image),(w,h)); self.rect= self.image.get_rect(topleft=(x,y))
#     def reset(self,surf): surf.blit(self.image,self.rect.topleft)
#     def collidepoint(self,pos): return self.rect.collidepoint(pos)
# # Backgrounds, Rules
# class Backgrounds(pygame.sprite.Sprite):
#     def __init__(self,pic,w,h,x,y): super().__init__(); self.image=pygame.transform.scale(pygame.image.load(pic),(w,h)); self.rect=self.image.get_rect(topleft=(x,y))
#     def reset(self,surf): surf.blit(self.image,self.rect.topleft)
# class Rules:
#     def __init__(self,text): self.font=pygame.font.SysFont('serif',20); self.image=self.font.render(text,True,WHITE)
#     def draw(self,surf,k): surf.blit(self.image,(320,120+30*k))
# # Starfield etc.
# class Star2:
#     def __init__(self): self.pos3d=self._rand(); self.vel=random.uniform(0.05,0.25); self.color=random.choice(COLORS)
#     def _rand(self): angle=random.uniform(0,2*math.pi);r=random.randrange(HEIGHT//35,HEIGHT)*35;return pygame.math.Vector3(r*math.cos(angle),r*math.sin(angle),Z_DISTANCE)
#     def update(self):
#         self.pos3d.z-=self.vel; self.pos3d= self._rand() if self.pos3d.z<1 else self.pos3d
#         self.screen_pos=pygame.math.Vector2(self.pos3d.x,self.pos3d.y)/self.pos3d.z+pygame.math.Vector2(WIDTH//2,HEIGHT//2)
#         self.size=(Z_DISTANCE-self.pos3d.z)/(0.2*self.pos3d.z)
#     def draw(self,surf): pygame.draw.rect(surf,self.color,(*self.screen_pos,self.size,self.size))
#
# class Fon:
#     def __init__(self,w,h,count):
#         self.surf=pygame.Surface((w,h))
#         self.surf.set_alpha(255)
#         self.stars=[Star2() for _ in range(count)]
#     def update(self,surf):
#         self.surf.fill(BLACK)
#         for s in self.stars: s.update(); s.draw(self.surf)
#         surf.blit(self.surf,(0,0))
#
# class Starfield(Fon):
#     def __init__(self): super().__init__(*RES,NUM_STARS); self.surf.set_alpha(ALPHA)
#     def run(self,surf): super().update(surf)
#




# from pygame import *
# import pygame as pg
# from constants import *
# from base_sprite import *
# from random import randint
# import random
# import math
#
#
# # создание окна
# window = display.set_mode((win_width, win_height))
# # установка названия
# display.set_caption(txt_caption)
#
#
# # класс фона для текста
# class Screensaver():
#   def __init__(self, x=0, y=0, width=10, height=10, color=None):
#       self.rect = Rect(x, y, width, height) #прямоугольник
#       self.fill_color = color
#
#
#   def fill(self):
#       draw.rect(window, self.fill_color, self.rect)
#
#
# '''класс надпись'''
# font.init()
# class Label(Screensaver):
#   def set_text(self, text, fsize, text_color):
#       self.image = font.SysFont('serif', fsize).render(text, True, text_color)
#
#
#   def draw(self, shift_x=0, shift_y=0):
#       self.fill()
#       window.blit(self.image, (self.rect.x + shift_x, self.rect.y + shift_y))
#
#
#  # кнопки заставки-меню
# class  Menu(GameSprite):
#  def __init__(self, player_image, player_x, player_y, size_x, size_y):
#      GameSprite.__init__(self, player_image, player_x, player_y,size_x, size_y)
# #  расположение на экране кнопок
#  def reset(self):
#        window.blit(self.image, (self.rect.x, self.rect.y))
#
#
# # проверка на нажатие кнопки
#  def collidepoint(self, x, y):
#       return self.rect.collidepoint(x, y)
#
#
# #  класс фонов
# class Backgrounds(sprite.Sprite):
#     def __init__(self, picture, w, h, x, y):
#         super().__init__()
#         self.pic = picture
#         self.image = transform.scale(image.load(self.pic), (w, h))
#         self.rect = self.image.get_rect()
#         self.rect.x = x
#         self.rect.y = y
#
#
#     def reset(self):
#         window.blit(self.image, (self.rect.x, self.rect.y))
#
#
# #  класс для написания правил к игре
# class Rules():
#      def __init__(self, text):
#          self.text = text
#          self.color = WHITE
#          self.image = font.SysFont('serif', 20).render(self.text, True, self.color)
#
#
#      def draw(self, k):
#          self.y = 120
#          window.blit(self.image, (320, self.y + 30*k))
#
#
# # класс главного фона во втором уровне
# class Fon():
#     def __init__(self, w, h, stars_count = 3000) -> None:
#         self.w = w
#         self.h = h
#         self.x = -1000
#         self.y = -200
#         self.image = Surface((w, h))
#         self.rect = self.image.get_rect()
#         self.stars_count = stars_count
#         self.stars = []
#         self.fill_stars()
#
#     # заполнение звёздам
#     def fill_stars(self):
#         for i in range(self.stars_count):
#             self.stars.append(Star(self.w, self.h))
#
#
#     def update(self, scr):
#         self.image.fill(BLACK)
#         for star in self.stars:
#             star.update()
#             self.image.blit(star.image, (star.rect.x, star.rect.y))
#         scr.blit(self.image, (self.x, self.y))
#
#
#
# class Star(sprite.Sprite):
#     def __init__(self, w, h ) -> None:
#         super().__init__()
#         self.r = randint(1,2)
#         self.image =  Surface((self.r*2,self.r*2), SRCALPHA)
#         self.rect = self.image.get_rect()
#         self.rect.x = randint(0, w)
#         self.rect.y = randint(1, h)
#         self.color = (255, 255, 255, 255)
#         self.shine_speed = randint(1,100)
#         self.shine_deep = randint(150,250)
#         self.shine_revers = False
#         self.shine_ok = randint(0,1)
#
#
#     def update(self):
#         if self.shine_ok == 1: self.color = self.__shine()
#         draw.circle(self.image, self.color, (self.r, self.r), self.r)
#
#
#     def __shine(self):
#         # моргание звезд - зависит от shine_speed и shine_deep
#         # которые создаются случайно для каждой звезды
#         color = self.color[3]
#         if self.shine_revers:
#             color += self.shine_speed
#             if color >= 255:
#                 color = 255
#                 self.shine_revers = False
#         else:
#             color -= self.shine_speed
#             if color <= 255 - self.shine_deep:
#                 color = 255 - self.shine_deep
#                 self.shine_revers = True
#         return tuple(list(self.color)[0:3] + [color])
#
#
#
# vec2, vec3 = pg.math.Vector2, pg.math.Vector3
# CENTER = vec2(WIDTH // 2, HEIGHT // 2)
#
#
# class Star2():
#     def __init__(self):
#         self.screen = window
#         self.pos3d = self.get_pos3d()
#         self.vel = random.uniform(0.05, 0.25)
#         self.color = random.choice(COLORS)
#         self.screen_pos = vec2(0, 0)
#         self.size = 10
#
#
#     def get_pos3d(self, scale_pos=35):
#         angle = random.uniform(0, 2 * math.pi)
#         radius = random.randrange(HEIGHT // scale_pos, HEIGHT) * scale_pos
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         return vec3(x, y, Z_DISTANCE)
#
#
#     def update(self):
#         self.pos3d.z -= self.vel
#         self.pos3d = self.get_pos3d() if self.pos3d.z < 1 else self.pos3d
#
#         self.screen_pos = vec2(self.pos3d.x, self.pos3d.y) / self.pos3d.z + CENTER
#         self.size = (Z_DISTANCE - self.pos3d.z) / (0.2 * self.pos3d.z)
#         # rotate xy
#         self.pos3d.xy = self.pos3d.xy.rotate(0.2)
#         # mouse
#         # mouse_pos = CENTER - vec2(pg.mouse.get_pos())
#         # self.screen_pos += mouse_pos
#
#
#     def draw(self):
#         s = self.size
#         if (-s < self.screen_pos.x < WIDTH + s) and (-s < self.screen_pos.y < HEIGHT + s):
#             pg.draw.rect(self.screen, self.color, (*self.screen_pos, self.size, self.size))
#             # pg.draw.rect(self.screen, self.color, self.size)
#
#
# # класс главного фона у 3 уровня
# class Starfield():
#     def __init__(self):
#         self.alpha_surface = pg.Surface(RES)
#         self.alpha_surface.set_alpha(ALPHA)
#         self.stars = [Star2() for i in range(NUM_STARS)]
#
#
#     def run(self):
#         [star.update() for star in self.stars]
#         self.stars.sort(key=lambda star: star.pos3d.z, reverse=True)
#         [star.draw() for star in self.stars]
#
#
# starfield = Starfield()
