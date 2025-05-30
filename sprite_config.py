import os
import pygame
import random

# Функция для получения размеров изображения
def get_image_size(image_path):
    image = pygame.image.load(image_path)
    return image.get_width(), image.get_height()


def parse_astr_collections(base_path='images/astr'):
    # Группируем изображения по префиксу (например, col5_1.png, col5_2.png -> коллекция col5)
    collections = {}
    for img in os.listdir(base_path):
        if img.endswith('.png'):
            # Извлекаем префикс имени файла (например, 'col5' из 'col5_1.png')
            prefix = img.split('_')[0]
            if prefix not in collections:
                collections[prefix] = []
            collections[prefix].append(os.path.join(base_path, img))

    # Преобразуем словарь в список коллекций
    return list(collections.values())


def parse_robots_collections(base_path='images/robots'):
    # Все роботы в одной коллекции (один список изображений)
    return [
        [os.path.join(base_path, img) for img in os.listdir(base_path) if img.endswith('.png')]
    ]


def parse_alians_collections(base_path='images/alians'):
    # Аналогично astr, группируем по префиксу
    collections = {}
    for img in os.listdir(base_path):
        if img.endswith('.png'):
            prefix = img.split('_')[0]
            if prefix not in collections:
                collections[prefix] = []
            collections[prefix].append(os.path.join(base_path, img))
    return list(collections.values())


def parse_nlo_collections(base_path='images/nlo'):
    # Аналогично astr, группируем по префиксу
    collections = {}
    for img in os.listdir(base_path):
        if img.endswith('.png'):
            prefix = img.split('_')[0]
            if prefix not in collections:
                collections[prefix] = []
            collections[prefix].append(os.path.join(base_path, img))
    return list(collections.values())

# def parse_planets(base_path='images/planets'):
#     planets = [os.path.join(base_path, img) for img in os.listdir(base_path) if img.endswith('.gif')]
#     return {i + 1: planet for i, planet in enumerate(planets)}

def parse_planets(base_path='images/planets'):
    planets = {}
    for i, img in enumerate(sorted([f for f in os.listdir(base_path) if f.endswith('.gif')]), 1):
        img_path = os.path.join(base_path, img)
        # width, height = get_image_size(img_path)
        planets[i] = {
            'id': i,
            'image': img_path,
            'name': f"Planet {i}",
            'discovered': False,
        }
    return planets

def create_sprite_config(collections, player_image, player_size, final, size_mapping=None):
    config = {
        'player': player_image,
        'player_size': player_size,
        'enemies': [],
        'final': final
    }
    for collection in collections:
        for img in collection:
            # Определяем размеры для изображения
            if size_mapping:
                filename = os.path.basename(img)
                size = size_mapping.get(filename, get_image_size(img))
            else:
                size = get_image_size(img)

            config['enemies'].append({
                'image': img,
                # 'width': size[0],
                # 'height': size[1]
                'width': 35,
                'height': 35
            })
    return config


# Задаем индивидуальные размеры для определенных изображений
astr_size_mapping = {
    # 'col5_1.png': (45, 45),
    # 'col5_2.png': (45, 45),
    # 'col6_1.png': (45, 45),

}

astr_collections = parse_astr_collections()
robots_collections = parse_robots_collections()
alians_collections = parse_alians_collections()
nlo_collections = parse_nlo_collections()
planets = parse_planets()

SPRITE_SETS = {
    'EASY': create_sprite_config(
        collections=nlo_collections,
        player_image='images/sheep3.png',
        player_size=(40, 35),
        final='images/2537512610.gif',
        size_mapping=astr_size_mapping
    ),
    'MEDIUM': create_sprite_config(
        collections=robots_collections,
        player_image='images/sprite1_1.png',
        player_size=(33, 35),
        final={'image': 'images/heart.png', 'width': 55, 'height': 50}
    ),
    'HARD': create_sprite_config(
        collections=alians_collections,
        player_image='images/sprite1_1.png',
        player_size=(28, 32),
        final={'image': 'images/sprite_girl.png', 'width': 40, 'height': 40}
    ),
    'EXPLORE': {
        'player': 'images/sheep3.png',
        'player_size': (35, 30),
        'enemies': [
            {'image': img, 'width': 35, 'height': 35}
            for collection in astr_collections + nlo_collections for img in collection
        ],
        'finals': planets
    }
}


# SPRITE_SETS = {
#     'EASY': {
#         'player': 'images/sheep3.png',
#         'player_size': (40, 35),
#         'enemies': [
#
#
#             # {'image': 'images/astr/col2_1.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_2.png','width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_3.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_4.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_5.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_6.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_7.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col2_8.png', 'width': 45, 'height': 45},
#
#
#             # {'image': 'images/astr/col3_1.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_2.png','width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_3.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_4.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_5.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_6.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_7.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col3_8.png', 'width': 45, 'height': 45},
#
#             # {'image': 'images/astr/col4_1.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col4_2.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col4_3.png', 'width': 45, 'height': 45},
#             # {'image': 'images/astr/col4_4.png', 'width': 45, 'height': 45},
#
#             {'image': 'images/astr/col5_1.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col5_2.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col5_3.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col5_4.png', 'width': 45, 'height': 45},
#
#             {'image': 'images/astr/col6_1.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col6_2.png','width': 45, 'height': 45},
#             {'image': 'images/astr/col6_3.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col6_4.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col6_5.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col6_6.png', 'width': 45, 'height': 45},
#
#             {'image': 'images/astr/col7_1.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col7_2.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col7_3.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col7_4.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col7_5.png', 'width': 45, 'height': 45},
#
#             {'image': 'images/astr/col8_1.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col8_2.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col8_3.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col8_4.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col8_5.png', 'width': 45, 'height': 45},
#             {'image': 'images/astr/col8_6.png', 'width': 45, 'height': 45}
#
#         ],
#         'final': 'images/2537512610.gif'
#     },
#     'MEDIUM': {
#         'player': 'images/sprite1_1.png',
#         'player_size': (33, 35),
#         'enemies': [
#             {'image': 'images/robots/robot1.png', 'width': 40, 'height': 40},
#             {'image': 'images/robots/robot2.png', 'width': 40, 'height': 40},
#             {'image': 'images/robots/robot3.png', 'width': 33, 'height': 47},
#             {'image': 'images/robots/robot4.png', 'width': 33, 'height': 47},
#             {'image': 'images/robots/robot5.png', 'width': 33, 'height': 47},
#             {'image': 'images/robots/robot6.png', 'width': 33, 'height': 47},
#             {'image': 'images/robots/robot7.png', 'width': 33, 'height': 47},
#             {'image': 'images/robots/robot8.png', 'width': 35, 'height': 45},
#             {'image': 'images/robots/robot9.png', 'width': 35, 'height': 45}
#
#         ],
#         'final': {'image': 'images/heart.png', 'width': 55, 'height': 50}
#     },
#     'HARD': {
#         'player': 'images/sprite1_1.png',
#         'player_size': (28, 32),
#         'enemies': [
#             # {'image': 'images/alians/al1_1.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al1_2.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al1_3.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al1_4.png', 'width': 30, 'height': 33},
#
#             # {'image': 'images/alians/al2_1.png', 'width': 28, 'height': 33},
#             # {'image': 'images/alians/al2_2.png', 'width': 28, 'height': 33},
#             # {'image': 'images/alians/al2_3.png', 'width': 28, 'height': 33},
#             # {'image': 'images/alians/al2_4.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al2_5.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al2_6.png', 'width': 30, 'height': 33},
#
#             # {'image': 'images/alians/al3_1.png', 'width': 30, 'height': 33},
#             # {'image': 'images/alians/al3_2.png', 'width': 32, 'height': 33},
#             # {'image': 'images/alians/al3_3.png', 'width': 32, 'height': 33},
#             # {'image': 'images/alians/al3_4.png', 'width': 32, 'height': 33},
#
#             {'image': 'images/alians/al4_1.png', 'width': 28, 'height': 33},
#             {'image': 'images/alians/al4_2.png', 'width': 28, 'height': 33},
#             {'image': 'images/alians/al4_3.png', 'width': 28, 'height': 33},
#             {'image': 'images/alians/al4_4.png', 'width': 28, 'height': 33},
#             {'image': 'images/alians/al4_5.png', 'width': 28, 'height': 33},
#
#
#         ],
#     'final': {'image': 'images/sprite_girl.png', 'width': 40, 'height': 40}
#     },
#     'EXPLORE': {
#         'player': 'images/sheep3.png',
# 'player_size': (35, 30),
#         'enemies': [
#             # {'image': 'images/nlo/nlo1_1.png', 'width': 35, 'height': 35},
#             # {'image': 'images/nlo/nlo1_2.png', 'width': 33, 'height': 35},
#             # {'image': 'images/nlo/nlo1_3.png', 'width': 35, 'height': 35},
#             # {'image': 'images/nlo/nlo1_4.png', 'width': 35, 'height': 30},
#             # {'image': 'images/nlo/nlo1_5.png', 'width': 35, 'height': 30},
#             #
#             # {'image': 'images/nlo/nlo2_1.png', 'width': 35, 'height': 30},
#             # {'image': 'images/nlo/nlo2_2.png', 'width': 37, 'height': 33},
#             # {'image': 'images/nlo/nlo2_3.png', 'width': 37, 'height': 33},
#             # {'image': 'images/nlo/nlo2_4.png', 'width': 37, 'height': 33},
#
#             # {'image': 'images/nlo/nlo3_1.png', 'width': 35, 'height': 30},
#             # {'image': 'images/nlo/nlo3_2.png', 'width': 33, 'height': 36},
#             # {'image': 'images/nlo/nlo3_3.png', 'width': 33, 'height': 36},
#             # {'image': 'images/nlo/nlo3_4.png', 'width': 33, 'height': 36},
#             # {'image': 'images/nlo/nlo3_5.png', 'width': 35, 'height': 30},
#             # {'image': 'images/nlo/nlo3_6.png', 'width': 37, 'height': 33},
#             # {'image': 'images/nlo/nlo3_7.png', 'width': 35, 'height': 35},
#             # {'image': 'images/nlo/nlo3_8.png', 'width': 35, 'height': 35},
#             # {'image': 'images/nlo/nlo3_9.png', 'width': 35, 'height': 35},
#
#             {'image': 'images/nlo/nlo4_1.png', 'width': 35, 'height': 33},
#             {'image': 'images/nlo/nlo4_2.png', 'width': 35, 'height': 33},
#             {'image': 'images/nlo/nlo4_3.png', 'width': 35, 'height': 30},
#             {'image': 'images/nlo/nlo4_4.png', 'width': 35, 'height': 30},
#             {'image': 'images/nlo/nlo4_5.png', 'width': 35, 'height': 30}
#
#         ],
#         # 'final_pool': [f'images/planet_explore{i}.gif' for i in range(1, 21)]  # 20 уникальных финальных спрайтов
#         'finals': {
#                     1: 'images/planets/1.gif',
#                     2: 'images/planets/2.gif',
#                     3: 'images/planets/3.gif',
#                     4: 'images/planets/4.gif',
#                     5: 'images/planets/5.gif',
#                     6: 'images/planets/6.gif',
#                     7: 'images/planets/7.gif',
#                     8: 'images/planets/8.gif',
#                     9: 'images/planets/9.gif',
#                     10: 'images/planets/10.gif',
#                     11: 'images/planets/11.gif',
#                     12: 'images/planets/12.gif',
#                     13: 'images/planets/13.gif',
#                     14: 'images/planets/14.gif',
#                     15: 'images/planets/15.gif',
#                     16: 'images/planets/16.gif',
#                     17: 'images/planets/17.gif',
#                     18: 'images/planets/18.gif',
#                     19: 'images/planets/19.gif',
#                     20: 'images/planets/20.gif'
#                  }
#     }
# }
