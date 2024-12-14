import time

FOLDER_NAME = 'wasp_ab'

# Screen regions
BATTLE_REGION = (0, 0, 177, 201)
LOOT_REGION = (760, 360, 975, 556)
HUNGER_REGION = (1749, 285, 1857, 294)
BACKPACK_REGION = (0, 317, 155, 504)
MAP_REGION = (1751, 26, 1858, 134)

# Colors and positions
COLOR_MANA = (0, 63, 140)
POSITION_MANA = (878, 32)
COLOR_GREEN_HEALTH = (100, 145, 4)
POSITION_HEALTH = (195, 35)

# Movement
MOVEMENT_KEYS = ('up', 'down', 'left', 'right')

# Images
PLAYER_IMG = 'imgs/player_point.png'
ANCHOR_IMG = 'imgs/anchor_floor3.png'
HOLE_IMG = 'imgs/hole.png'
LOOT_IMG = 'imgs/loot_wasp2.png'
EMPTY_BATTLE_IMG = 'imgs/empty_battle3.png'
ATTACKING_IMG = 'imgs/attacking6.png'
FOOD_IMG = 'imgs/brown_mushroom.png'
HUNGER_IMG = 'imgs/hungry.png'

# Timing
last_attack = time.time()
attack_cooldown = 5
running = True