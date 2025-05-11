from config import win_width as W, win_height as H, txt_welcome, txt_select, txt_win, BLACK_BLUE, WHITE, GREY_BLUE, \
    DARK_BLUE
from game_music import mixer
import pygame as pg


class Instance:
    def __init__(self, src, *args):
        self.__src = src
        if (len(args) != 4): raise AttributeError('Надо передать 4 параметра: x, y, width, height')
        for arg in args:
            if type(arg) not in (int, float): raise TypeError
        self.__args = (src,) + tuple(map(int, args))

    def __iter__(self):
        return iter(self.__args)


class Img:
    def __init__(self, src):
        self.__img = pg.image.load(src)

    def __get__(self, *args, **kwargs):
        return self.__img


class Sound:
    def __init__(self, src):
        self.__sound = mixer.music.load(src)
        self.__src = src

    def __get__(self, *args, **kwargs):
        return self.__src


class Text:
    def __init__(self, text, color, font_size):
        self.__text = text
        self.__color = color
        self.__font_size = font_size

    def __iter__(self):
        return iter((self.__text, self.__color, self.__font_size))


if __name__ != '__config__':
    class LoseState:
        bg = Instance('images\\lose.jpg', W, H, 0, 0)
        back = Instance('images\\menu.png', 30, 380, 130, 135)
        reset = Instance('images\\restart.png', 520, 390, 120, 120)
        lose_label = Img('images\\textlose.png')


    class MenuState:
        bg = Instance('images\\m_start_back2.jpg', W + 20, H + 20, -10, 0)
        start = Instance('images\\start.png', 550, 370, 130, 130)
        cross = Img('images/red_cross.png')
        manual = Instance('images\\instruction.png', 380, 395, 110, 110)
        sound = Instance('images\\sound.png', 185, 365, 170, 170)
        label = [140, 0, 680, 40, BLACK_BLUE]
        music = Sound('sound\\menu.mp3')
        greetings = Text(txt_welcome, 62, WHITE)
        stars = {
            'count': 100,
            'min_speed': 0.5,
            'max_speed': 0.8,
            'min_size': 1.0,
            'max_size': 3.0
        }
        title = {
            'text': 'CosmoMan',
            'font_size': 100,
            'pulsation': True,
            'reflection': True,
            'flash_probability': 0.01,
            'color_change_speed': 0.02
        }
        buttons = {
            'names': ["START", "CONTROLS", "FOUND PLANETS", "RATING"],
            'vertical_spacing': 50,
            'top_margin': 270,
            'width': 350,
            'height': 60,
            'base_color': (100, 200, 255, 150),
            'hover_color': (255, 255, 255, 200),
            'bg_color': (0, 0, 50, 100),
            'glow_transparency': 30,
            'glow_size': 15,
            'inactive_color': (150, 150, 150, 100),
            'inactive_bg_color': (0, 0, 30, 50)
        }


    class LevelSelectState:
        bg = Instance('images\\select.jpg', W + 20, H + 20, -10, 0)
        btn = [
            Instance('images\\select1.png', 170, 120, 190, 100),
            Instance('images\\select2.png', 170, 250, 190, 100),
            Instance('images\\select3.png', 170, 375, 190, 100),
        ]
        explore = Instance('images\\explore.png', 400, 375, 190, 100)
        # back = Instance('images\\menu.png', 70, 420, 100, 100)
        back = Instance('images\\menu.png', 185, 365, 100, 100)
        pre_init_back_label = (140, 0, 680, 40, GREY_BLUE)
        back_label = Text(txt_select, 62, WHITE)
        music = Sound('sound\\menu.mp3')
        stars = {
            'count': 100,
            'min_speed': 0.5,
            'max_speed': 0.8,
            'min_size': 1.0,
            'max_size': 3.0
        }
        title = {
            'text': 'SELECT LEVEL',
            'font_size': 80,
            'pulsation': True,
            'reflection': False,
            'flash_probability': 0.01,
            'color_change_speed': 0.01
        }
        buttons = {
            'names': ["LEVEL1", "LEVEL2", "LEVEL3", "EXPLORE UNIVERSITY"],
            'vertical_spacing': 50,
            'top_margin': 270,
            'width': 450,
            'height': 60,
            'base_color': (100, 200, 255, 150),
            'hover_color': (255, 255, 255, 200),
            'bg_color': (0, 0, 50, 100),
            'glow_transparency': 30,
            'glow_size': 15,
            'inactive_color': (150, 150, 150, 100),
            'inactive_bg_color': (0, 0, 30, 50)
        }


    class PauseState:
        bg = Instance('images\\pause.jpg', W + 20, H, 0, 0)
        resume = Instance('images\\start.png', 350, 380, 150, 150)
        back = Instance('images\\menu.png', 100, 370, 130, 135)


    class PlayState:
        hp = (10, 0, 70, 30, BLACK_BLUE)
        music = Sound('sound\\fon1.mp3')

        @staticmethod
        def hp_text(player):
            return Text(f'Жизни: {player.lives} Бонусы: {player.collected_prizes} Пули: {player.limit}', 20, WHITE)


    class WinState:
        bg = Instance('images\\win.jpg', W, H, 0, 0)
        back_label = (230, 5, 200, 50, DARK_BLUE)
        per_init_back_label = (txt_win, 55, WHITE)
        back = Instance('images\\menu.png', 30, 380, 130, 135)
        restart = Instance('images\\restart.png', 520, 390, 120, 120)


    class LoginState:
        stars = {
            'count': 100,
            'min_speed': 0.5,
            'max_speed': 0.8,
            'min_size': 1.0,
            'max_size': 3.0
        }
        title = {
            'text': "Start the Space Adventure",
            'font_size': 55,
            'pulsation': False,
            'reflection': True,
            'flash_probability': 0.01,
            'color_change_speed': 0.01
        }
        # title = (W // 2 - 200, H // 2 - 150, 400, 50, (255, 255, 255))
        username_box = (W // 2 - 150, H // 2 - 50, 300, 40, "User name", (200, 200, 200), (255, 255, 255))
        password_box = (W // 2 - 150, H // 2 + 20, 300, 40, "Password", (200, 200, 200), (255, 255, 255))
        login_btn = ("images/login_btn.png", W // 2 - 120, H // 2 + 100, 100, 50)
        register_btn = ("images/register_btn.png", W // 2 + 120, H // 2 + 100, 100, 50)
        message = (W // 2 - 150, H // 2 + 180, 300, 30, (255, 0, 0))
        # label = ("Космическое Приключение", 36, (255, 255, 255))
        msg = ("", 24, (255, 0, 0))


    class PopupState:
        instruction = Img("images\\instr.jpg")
        cross = Instance("images\\cross.png", W - 50, 20, 30, 30)
        decoration = Img("images\\popup_decor.png")


    class IntroState:
        starfield = {
            'num_stars': 1000,
            'vel_min': 1.0,
            'vel_max': 6.0,
            'colors': ['blue', 'cyan', 'skyblue', 'purple', 'magenta'],
            'scale_pos': 35,
            'alpha': 30,
            'rotation_base': 0.5,
            'duration': 3.0
        }
        color_sets = {
            'cool': ['blue', 'cyan', 'skyblue', 'purple', 'magenta'],
            'warm': ['red', 'orange', 'yellow', (255, 215, 0), (220, 20, 60)],
            'pastel': [(230, 230, 250), (152, 255, 152), (255, 218, 185), (137, 207, 240), (255, 182, 193)],
            'monochrome': ['white', (211, 211, 211), (105, 105, 105), 'black'],
            'neon': [(57, 255, 20), (255, 105, 180), (255, 255, 0), (255, 69, 0)]
        }