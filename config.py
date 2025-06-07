W = win_width = 1100
H = win_height = 800
RES = WIDTH, HEIGHT = 1100, 800
NUM_STARS = 100
#COLORS1 = 'red green blue orange purple cyan'.split()
COLORS1 = 'red|green|blue|orange|purple'
COLORS = COLORS1.split("|")
Z_DISTANCE = 80
ALPHA = 300
WALL_OFFSET = 1

y_offset = 140
x_offset = W//2 - 60
padding = 180

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


scores = {
    'EASY': 5.0,
    'MEDIUM': 10.0,
    'HARD': 15.0,
    'EXPLORE': 20.0,
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

serv = {
    # 'host': '127.0.0.1',
'host': '107.189.15.175',
    'port': 8081,
}

# mapped = {
#     'EASY': 'легкого лабиринта',
#     'MEDIUM': 'среднего лабиринта',
#     'HARD': 'тяжелого лабиринта',
#     'EXPLORE': 'экстримального лабиринта'
# }

mapped = {
    'EASY': 'легкого лабиринта (корабль поврежден, нужно срочно долететь до Земли, избегая астероидов и инопланетян)',
    'MEDIUM': 'среднего лабиринта (космонавт проник в заброшенный технозавод за двигателем, но там охраняют роботы)',
    'HARD': 'пришельцы похитили напарницу, нужно прорваться через их базу',
    'EXPLORE': 'космический корабль готов лететь на новую планету. и описать что за планета будет'
}
# .tables                 -- показать таблицы
# SELECT * FROM table_name; -- вывести данные таблицы
# .quit                   -- выйти
# story_tone = {
#     'EASY': 'напряженный, но с надеждой на спасение',
#     'MEDIUM': 'мрачный, техногенный, с угрозой роботов',
#     'HARD': 'агрессивный, отчаянный, с мотивом спасения',
#     'EXPLORE': 'таинственный, с оттенком научной фантастики'
# }

key = "sk-a2b62469cef64d60b4b52f1b65b7bb96"

FPS = 60

"""
21, 14
20, 14
16, 13
21, 14
17, 12
19, 15
18, 11
18, 12
17, 14
18, 12
18, 14
19, 13
21, 15
19, 14
15, 14
22, 13
19, 12
"""

grid_sizes = {
    'EASY': (14, 11),
    'MEDIUM': (16, 12),
    # 'MEDIUM': (24, 18),
    # 'HARD': (24, 15),
    # 'HARD': (19, 15),
    'HARD': (18, 12),
    # 'EXPLORE': (22, 13)
}