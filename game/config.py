import pygame
import os

pygame.font.init()

# Lấy thư mục chứa file py hiện tại
current_dir = os.path.dirname(__file__)

# Lấy thư mục cha chứa thư mục `fonts` và `images`
parent_dir = os.path.dirname(current_dir)

# Width and height of the application
WIN_WIDTH = 1200
WIN_HEIGHT = 900

# Red side, blue side indicator
RED_SIDE = RED_TURN = 1
BLUE_SIDE = BLUE_TURN = 0

background_image = pygame.image.load("images/background/background.jpg")
background_image = pygame.transform.scale(background_image, (WIN_WIDTH, WIN_HEIGHT))
overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT))
overlay.fill((255, 255, 255))
overlay.set_alpha(75)


class Color:
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 255, 0)
    YELLOW = (255, 255, 0)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    PURPLE = (128, 0, 128)
    ORANGE = (255, 165, 0)
    GREY = (128, 128, 128)
    TURQUOISE = (64, 224, 208)
    DARK_YELLOW = (252, 182, 40)

class Font:
    SCORE_TEXT_FONT = pygame.font.Font(os.path.join(parent_dir, "fonts", "CursedTimerUlil-Aznm.ttf"), 30)
    SCORE_FONT = pygame.font.Font(os.path.join(parent_dir, "fonts", "CursedTimerUlil-Aznm.ttf"), 30)
    SCORE_FONT.set_bold(True)
    NORMAL_FONT = pygame.font.Font(os.path.join(parent_dir, "fonts", "Poppins-Bold.ttf"), 30)
    TITLE_FONT = pygame.font.Font(os.path.join(parent_dir, "fonts", "Allison-Regular.ttf"), 120)
    WRITING_FONT = pygame.font.Font(os.path.join(parent_dir, "fonts", "Allison-Regular.ttf"), 30)


class ChessImages:
    RED_CHARIOT = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-car.png"))
    RED_CANNON = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-cannon.png"))
    RED_HORSE = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-horse.png"))
    RED_ELEPHANT = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-elephant.png"))
    RED_SOLDIER = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-pawn.png"))
    RED_ADVISOR = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-bodyguard.png"))
    RED_LORD = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "red-king.png"))

    BLUE_CHARIOT = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-car.png"))
    BLUE_CANNON = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-cannon.png"))
    BLUE_HORSE = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-horse.png"))
    BLUE_ELEPHANT = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-elephant.png"))
    BLUE_SOLDIER = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-pawn.png"))
    BLUE_ADVISOR = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-bodyguard.png"))
    BLUE_LORD = pygame.image.load(os.path.join(parent_dir, "images", "pieces", "blue-king.png"))
