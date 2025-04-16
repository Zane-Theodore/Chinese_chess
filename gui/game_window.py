import pygame
from utils.config import HEIGHT, WIDTH, tittle

def create_windown(width = WIDTH, height = HEIGHT, caption = tittle):
    pygame.init()
    screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
    pygame.display.set_caption(caption)
    return screen