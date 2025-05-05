# from pygame import *
# init()
#
#
# # создание фоновой музыки
# melody = 'sound\\fon1.mp3'
# mixer.music.load(melody)
# # установка громкости
# mixer.music.set_volume(0.2)
# # бесконечное повторение музыки
# mixer.music.play(-1)
# # звук при выстреле
# fire_mus = mixer.Sound('sound\\fire1.wav')
# # звук при сборе бонуса
# #star_mus = mixer.Sound('sound\\zvezda.mp3')
# star_mus = mixer.Sound('sound\\star.wav')
#

import pygame as pg

mixer = pg.mixer
mixer.init()

# def win():
#     sound = mixer.Sound('sound\\win.mp3')
#     sound.set_volume(0.2)
#     sound.play()
#
# def lose():
#     sound = mixer.Sound('sound\\lose.mp3')
#     sound.set_volume(0.2)
#     sound.play()