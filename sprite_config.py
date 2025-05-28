# В config_state.py или новом файле sprite_config.py
SPRITE_SETS = {
    'EASY': {
        'player': 'images/sheep3.png',
        'enemies': ['images/level1/as3.png', 'images/level1/alian1.png', 'images/level1/alian3.png', 'images/level1/alian4.png'],
        'final': 'images/2537512610.gif'
    },
    'MEDIUM': {
        'player': 'images/astronaut.png',
        'enemies': ['images/robot1.png', 'images/robot2.png', 'images/robot3.png', 'images/robot4.png', 'images/robot5.png'],
        'final': 'images/2537512610.gif'
    },
    'HARD': {
        'player': 'images/girl3.png',
        'enemies': ['images/alien1.png', 'images/alien2.png'],
        'final': 'images/2537512610.gif'
    },
    'EXPLORE': {
        'player': 'images/astronaut_explore.png',
        'enemies': ['images/alien_explore1.png', 'images/alien_explore2.png', 'images/alien_explore3.png'],
        # 'final_pool': [f'images/planet_explore{i}.gif' for i in range(1, 21)]  # 20 уникальных финальных спрайтов
        'finals': {
                    1: 'images/planet_explore1.gif',
                    2: 'images/planet_explore2.gif',
                    3: 'images/planet_explore3.gif',
                    # ... до 20 или нужного количества
                }
    }
}
# 'images/nlo6.png', 'images/nlo3.png', 'images/nlo4.png'