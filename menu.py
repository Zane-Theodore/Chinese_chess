import pygame
from game.config import Font, Color, WIN_HEIGHT, WIN_WIDTH, background_image, overlay

def main_menu():
    """
    Display main menu
    """

    with_player_rect = pygame.Rect(WIN_WIDTH // 2 - 150, 250, 300, 50) 
    with_ai_rect = pygame.Rect(WIN_WIDTH // 2 - 150, 350, 300, 50) 
    quit_rect = pygame.Rect(WIN_WIDTH // 2 - 150, 450, 300, 50)

    menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Chinese Chess")
    run = True

    while run:
        menu_win.blit(background_image, (0, 0))
        menu_win.blit(overlay, (0, 0))
        
        title = Font.TITLE_FONT.render("Chinese Chess", True, Color.BLACK)
        menu_win.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 100))

        pygame.draw.rect(menu_win, Color.RED, with_player_rect) 
        pygame.draw.rect(menu_win, Color.RED, with_ai_rect) 
        pygame.draw.rect(menu_win, Color.RED, quit_rect)

        play_with_player_text = Font.NORMAL_FONT.render("PLAY WITH PLAYER", True, Color.BLACK)
        play_with_ai_text = Font.NORMAL_FONT.render("PLAY WITH AI", True, Color.BLACK)
        quit_text = Font.NORMAL_FONT.render("QUIT", True, Color.BLACK)

        menu_win.blit(play_with_player_text, (with_player_rect.x + 20, with_player_rect.y + 10))
        menu_win.blit(play_with_ai_text, (with_ai_rect.x + 20, with_ai_rect.y + 10))
        menu_win.blit(quit_text, (quit_rect.x + 100, quit_rect.y + 10))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    pos = pygame.mouse.get_pos()
                    if with_player_rect.collidepoint(pos):
                        return "player_vs_player"
                    elif with_ai_rect.collidepoint(pos): 
                        return "player_vs_ai"
                    elif quit_rect.collidepoint(pos):
                        return "quit"

        pygame.display.flip()