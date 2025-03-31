import pygame

from game.config import Color, WIN_HEIGHT, WIN_WIDTH, background_image, overlay
from game.controlPanel import ControlPanel
from game.game import Game
from menu import main_menu


# Increase sharpness
import ctypes

ctypes.windll.shcore.SetProcessDpiAwareness(1)

WIN = pygame.display.set_mode(
    (WIN_WIDTH, WIN_HEIGHT), pygame.RESIZABLE
)  # initilize win form
pygame.display.set_caption("Chinese Chess Game")  # win caption
pygame.font.init()
myfont = pygame.font.SysFont("Comic Sans MS", 15)

def draw(game, controlPanel):
    """
    Drawing the game to window
    """
    WIN.blit(background_image, (0, 0))
    WIN.blit(overlay, (0, 0))
    game.updateGame()

    controlPanel.draw(WIN)
    pygame.display.update()

def main():
    """
    Main function
    """
    while True:
        choice = main_menu()

        game = Game(WIN)
        controlPanel = ControlPanel(game)
        run = True

        if choice == "player_vs_player":
            while run:
                draw(game, controlPanel)
                # Loop through all events in 1 frames
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        print("Quit game")
                        return

                    pos = pygame.mouse.get_pos()
                    if pygame.mouse.get_pressed()[0]:
                        if not game.isOver:
                            game.checkForMove(pos)
                        else:
                            print("Game is over")

                        controlPanel.checkForClick(pos)
        elif choice == "player_vs_ai":
            print("feather is creating . . .")
            continue
        elif choice == "quit":
            print("Quit game")
            pygame.quit()
            exit()

if __name__ == "__main__":
    main()