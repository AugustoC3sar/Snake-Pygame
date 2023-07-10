import pygame

# Font
pygame.font.init()
FONT = pygame.font.Font('PressStart2P.ttf', 20)

# Screen size
WIDTH, HEIGHT = 500, 540

# Window update ratio
FPS = 20

# Snake body size
PIXEL = 20

# Info height size
MARGIN = 40

# Game initialization
DEFAULT_HEAD = (60,60)
DEFAULT_BP1 = (40,60)
DEFAULT_BP2 = (20,60)

# Colors
HEAD_COLOR = (50,50,150)
BODY_COLOR = (100,100,200)
FRUIT_COLOR = (255,0,0)
MAZE_COLOR = (50,100,50)
FONT_COLOR = (255,255,255)
INFO_BG_COLOR = (30,50,30)
