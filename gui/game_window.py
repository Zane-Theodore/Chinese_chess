import pygame
from utils.config import HEIHGT, WIDTH, tittle

def create_windown(width = WIDTH, height = HEIHGT, caption = tittle):
    pygame.init()
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption(caption)
    return screen