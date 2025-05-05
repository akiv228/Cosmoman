# win_width = 710
# win_height = 540
win_width = 1100
win_height = 800
# RES = WIDTH, HEIGHT = 710, 540
RES = WIDTH, HEIGHT = 1100, 800
NUM_STARS = 100
#COLORS1 = 'red green blue orange purple cyan'.split()
# COLORS1 = 'red|green|blue|orange|purple'
COLORS1 = 'white'
COLORS = COLORS1.split("|")
Z_DISTANCE = 80
ALPHA = 300
WALL_OFFSET = 1

txt_caption = "Galactic maze"
txt_welcome = "Galactic maze"
txt_select = "Select Difficulty"
txt_select1 = "EASY"
txt_select2 = "MEDIUM"
txt_select3 = "HARD"
txt_win = "You win!"
instr = "Управление"
text_rules = {
1: 'Управление героем комбинацией стрелок',
2: 'Выстрел: пробел',
3: 'Пауза: ESC',
4: 'Музыка вкл./выкл.: "M"',
5: 'Постарайся собрать все бонусы-звёздочки!',
}

BLACK_BLUE = (28,39,71)
DARK_BLUE = (4, 60, 117)
WHITE = (255, 255, 255)
LIGHT_GREY = (192, 192, 192)
GREY_BLUE = (2, 65, 108)
BLACK = (0,0,0)

run = True
finish = False
flag = 'menu'
select = 0
check_sound = 0
paused = False

FPS = 60