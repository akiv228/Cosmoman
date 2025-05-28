# В config_state.py или новом файле sprite_config.py
SPRITE_SETS = {
    'EASY': {
        'player': 'images/sheep3.png',
        'player_size': (40, 35),
        'enemies': [
            {'image': 'images/level1/al1.png', 'width': 40, 'height': 30},
            {'image': 'images/level1/al2.png', 'width': 40, 'height': 35},
            {'image': 'images/level1/al3.png', 'width': 40, 'height': 35},
            {'image': 'images/level1/al5.png', 'width': 40, 'height': 30},
            {'image': 'images/level1/al6.png', 'width': 40, 'height': 35},
            {'image': 'images/level1/al7.png', 'width': 40, 'height': 35}
            # {'image': 'images/level1/alian1.png', 'width': 40, 'height': 30},
            # {'image': 'images/level1/alian2.png', 'width': 40, 'height': 35},
            # {'image': 'images/level1/alian3.png', 'width': 40, 'height': 35}


            # {'image': 'images/level1/as1.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as2.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as3.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as4.png', 'width': 35, 'height': 30},
            # {'image': 'images/level1/as5.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as6.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as7.png', 'width': 35, 'height': 35},

            # {'image': 'images/level1/as8.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as9.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as10.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as11.png', 'width': 35, 'height': 30},
            # {'image': 'images/level1/as12.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as1.png', 'width': 40, 'height': 40},
            # {'image': 'images/level1/as1.png', 'width': 40, 'height': 40}

        ],
        'final': 'images/2537512610.gif'
    },
    'MEDIUM': {
        'player': 'images/sprite1.png',
'player_size': (35, 35),
        'enemies': [
            # {'image': 'images/robot1.png', 'width': 50, 'height': 50},
            # {'image': 'images/robot2.png', 'width': 40, 'height': 40},
            # {'image': 'images/robot3.png', 'width': 40, 'height': 40},
            # {'image': 'images/robot4.png', 'width': 40, 'height': 40},
            # {'image': 'images/robot5.png', 'width': 40, 'height': 40}
            {'image': 'images/level1/as1.png', 'width': 50, 'height': 50},
            {'image': 'images/level1/alian1.png', 'width': 40, 'height': 40},
            {'image': 'images/level1/alian3.png', 'width': 40, 'height': 40},
            {'image': 'images/level1/alian2.png', 'width': 40, 'height': 40},
            {'image': 'images/level1/alian3.png', 'width': 40, 'height': 40},


            # {'image': 'images/level1/as8.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as9.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as10.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as11.png', 'width': 35, 'height': 30},
            # {'image': 'images/level1/as12.png', 'width': 35, 'height': 35},
            # {'image': 'images/level1/as1.png', 'width': 40, 'height': 40},
            # {'image': 'images/level1/as1.png', 'width': 40, 'height': 40}

        ],
        'final': {'image': 'images/sprite2.png', 'width': 40, 'height': 40}
    },
    'HARD': {
        'player': 'images/astronaut.png',
'player_size': (30, 30),
        'enemies': [
            # {'image': 'images/level1/as.png', 'width': 50, 'height': 50},
            # {'image': 'images/level1/alian1.png', 'width': 40, 'height': 40},
            # {'image': 'images/level1/alian3.png', 'width': 40, 'height': 40},
            # {'image': 'images/level1/alian2.png', 'width': 40, 'height': 40},
            # {'image': 'images/level1/alian3.png', 'width': 40, 'height': 40}
            {'image': 'images/level1/as1.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as2.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as3.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as4.png', 'width': 35, 'height': 30},
            {'image': 'images/level1/as5.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as6.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as7.png', 'width': 35, 'height': 35}
        ],
    'final': {'image': 'images/girl3.png', 'width': 50, 'height': 50}
    },
    'EXPLORE': {
        'player': 'images/sheep3.png',
'player_size': (40, 35),
        'enemies': [
            {'image': 'images/level1/as8.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as9.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as10.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as11.png', 'width': 35, 'height': 30},
            {'image': 'images/level1/as12.png', 'width': 35, 'height': 35},
            {'image': 'images/level1/as1.png', 'width': 40, 'height': 40},
            {'image': 'images/level1/as1.png', 'width': 40, 'height': 40}

        ],
        # 'final_pool': [f'images/planet_explore{i}.gif' for i in range(1, 21)]  # 20 уникальных финальных спрайтов
        'finals': {
                    1: 'images/planets/1.gif',
                    2: 'images/planets/2.gif',
                    3: 'images/planets/3.gif',
                    # ... до 20 или нужного количества
                }
    }
}
# 'images/nlo6.png', 'images/nlo3.png', 'images/nlo4.png'