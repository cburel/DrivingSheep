import pygame

# pygame properties
FRAME_RATE = 60
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 600
BACKGROUND_COLOR = (100, 149, 237)
BORDER_RADIUS = 50
BOUNDARY_FORCE = 1
CLOCK = pygame.time.Clock()
DELTATIME = CLOCK.tick(60) * .001 * FRAME_RATE

# agent properties
VECTOR_LINE_LENGTH = 25

#player properties
PLAYER_SIZE = 10
PLAYER_SPD = 2.5
PLAYER_COLOR = (255, 255, 0)
PLAYER_XPOS = DISPLAY_WIDTH / 2
PLAYER_YPOS = DISPLAY_HEIGHT / 2
PLAYER_TO_SHEEP_FORCE = 1

# enemy properties
ENEMY_SIZE = 10
ENEMY_SPD = 2
ENEMY_COLOR = (0, 255, 0)
MAX_ENEMIES = 10
FLEE_RANGE = 200
ENEMY_FLEE_FORCE = 1
ENEMY_WANDER_FORCE = 1