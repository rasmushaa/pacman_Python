'''
Created on 14 Jan 2020

@author: rasmus
'''




import  pygame
vec   = pygame.math.Vector2


GRID_ON         = False
ASTAR_VISUAL    = False
CAN_DIE         = True

# Nayttoasetukset
#WIDTH, HEIGHT = 750,825
WIDTH, HEIGHT = 610,670
TOP_BOTTOM_BUFFER = 50
MAZE_WIDTH, MAZE_HEIGHT = WIDTH - TOP_BOTTOM_BUFFER, HEIGHT - TOP_BOTTOM_BUFFER
FPS = 60

# Pisteasetukset
SCORE_GHOST         = 100
SCORE_POWERUP       = 50
SCORE_COIN          = 1

# Hahmoasetukset
PLAYER_LIVES        = 5
PLAYER_SPEED        = 1.1 * ((MAZE_HEIGHT/300))
RED_GHOST_SPEED     = 1.0 * ((MAZE_HEIGHT/300))
BLUE_GHOST_SPEED    = 0.8 * ((MAZE_HEIGHT/300))
PINK_GHOST_SPEED    = 0.9 * ((MAZE_HEIGHT/300))
ORANGE_GHOST_SPEED  = 0.9 * ((MAZE_HEIGHT/300))

# Vakiot
CELL_X = 28
CELL_Y = 30
POSSIBLE_DIRECTIONS = [vec(1, 0), vec(0, 1), vec(-1, 0), vec(0, -1)]
ALL_DIRECTION       = [vec(1, 0), vec(1, 1), vec(0, 1),  vec(-1, 1), vec(-1, 0), vec(-1, -1), vec(0, -1), vec(1, -1)]

# Variasetukset
BLACK           = (0,       0,      0)
WHITE           = (255,     255,    255)
GREY            = (107,     107,    107)
PLAYER_COLOR    = (255,     255,    0)
RED_GHOST       = (255,     0,      0)
PINK_GHOST      = (255,     185,    255)
ORANGE_GHOST    = (255,     185,    82)
BLUE_GHOST      = (0,       255,    255)
COIN_COLOR      = (220,     220,    220)
POWER_COLOR     = (240,     240,    240)


# Fonttiasetukset
START_TEXT_SIZE = 16
START_FONT = "arialblack"
