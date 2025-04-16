import pygame

tittle = "Chinese Chess"

pygame.font.init()

HEIGHT = 1000
WIDTH = 900
GAP = WIDTH // 9
river_words = ['楚河', '漢界']

class Color:
    RED = (255, 0, 0)
    BLUE = (10, 30, 210, 128)
    YELLOW = (255, 255, 0)
    DARK_YELLOW = (255, 165, 0)
    GREEN = (0, 80, 10, 128)
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRAY = (50, 50, 50)
    LiGHT_GRAY = (200, 200, 200)
    WHITE = (255, 255, 255)
    WHITE_WITH_ALPHA = (255, 255, 255, 10)
    ORANGE = (210, 100, 40)
    PURPLE = (35, 5, 170)
    SHADOW = (53, 75, 94)
    
class Font:
    TITTLE_FONT = pygame.font.Font("assets/font/vni 27 bendigo.ttf", 90)
    NORMAL_FONT = pygame.font.Font("assets/font/svn bango.ttf", 45)