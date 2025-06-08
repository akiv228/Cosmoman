import os
import pygame
import random


def get_image_size(image_path):
    image = pygame.image.load(image_path)
    return image.get_width(), image.get_height()


def parse_collections(base_path=None):
    collections = {}
    for img in os.listdir(base_path):
        if img.endswith('.png'):
            prefix = img.split('_')[0]
            if prefix not in collections:
                collections[prefix] = []
            collections[prefix].append(os.path.join(base_path, img))

    return list(collections.values())


def parse_robots_collections(base_path='images/robots'):
    return [
        [os.path.join(base_path, img) for img in os.listdir(base_path) if img.endswith('.png')]
    ]


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


def create_sprite_config(collections, player_image, player_size, final, collection_name=None):
    config = {
        'player': player_image,
        'player_size': player_size,
        'enemies': [],
        'final': final
    }

    for collection in collections:
        for img in collection:
            if collection_name and collection_name in COLLECTION_SIZES:
                size = COLLECTION_SIZES[collection_name]
            else:
                # size = get_image_size(img)
                (35, 35)

            config['enemies'].append({
                'image': img,
                'width': size[0],
                'height': size[1]
            })
    return config


astr_collections = parse_collections('images/astr')
robots_collections = parse_robots_collections()
alians_collections = parse_collections('images/alians')
nlo_collections = parse_collections('images/nlo')
planets = parse_planets()

COLLECTION_SIZES = {
    'astr': (35, 35),
    'robots': (33, 40),
    'alians': (30, 35),
    'nlo': (35, 35)
}

SPRITE_SETS = {
    'EASY': create_sprite_config(
        collections=nlo_collections,
        player_image='images/sheep3.png',
        player_size=(35, 33),
        final='images/2537512610.gif',
        collection_name='nlo'
    ),
    'MEDIUM': create_sprite_config(
        collections=robots_collections,
        player_image='images/sprite1_1.png',
        player_size=(28, 32),
        final={'image': 'images/heart.png', 'width': 55, 'height': 50},
        collection_name='robots'
    ),
    'HARD': create_sprite_config(
        collections=alians_collections,
        player_image='images/sprite1_1.png',
        player_size=(28, 32),
        final={'image': 'images/sprite_girl.png', 'width': 40, 'height': 40},
        collection_name='alians'
    ),
    'EXPLORE': {
        'player': 'images/sheep3.png',
        'player_size': (35, 30),
        'enemies': [
            {'image': img, 'width': 35, 'height': 35}
                for img in random.choice([
                [img for collection in astr_collections for img in collection],
                [img for collection in nlo_collections for img in collection]
            ])
            # for collection in astr_collections + nlo_collections for img in collection
        ],
        'finals': planets
    }
}
all_smoke_images = {
    'EASY': ['images/smoke/smoke2.png'],
    'MEDIUM': ['images/smoke/smoke4.png'],
    'HARD': [f'images/smoke/smoke{i}.png' for i in [2, 5]],
    'EXPLORE': [f'images/smoke/smoke{i}.png' for i in [3, 7, 8, 6, 9]]
}

# Задаем индивидуальные размеры для определенных изображений
astr_size_mapping = {
    # 'col5_1.png': (45, 45),
    # 'col5_2.png': (45, 45),
    # 'col6_1.png': (45, 45),

}


