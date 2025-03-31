import pygame
from game.config import Font, Color, WIN_HEIGHT, WIN_WIDTH, background_image, overlay

def main_menu():
    """
    Display main menu
    """

    # Cập nhật tọa độ y để nút trên cùng nằm ở nửa chiều cao cửa sổ
    with_player_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2, 300, 50) 
    with_ai_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 100, 300, 50) 
    quit_rect = pygame.Rect(WIN_WIDTH // 2 - 150, WIN_HEIGHT // 2 + 200, 300, 50)

    menu_win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Chinese Chess")
    run = True

    while run:
        menu_win.blit(background_image, (0, 0))
        menu_win.blit(overlay, (0, 0))
        
        # Render title
        title = Font.TITLE_FONT.render("Chinese Chess", True, Color.BLACK)
        menu_win.blit(title, (WIN_WIDTH // 2 - title.get_width() // 2, 75))

        # Draw buttons with black border and white background
        for rect in [with_player_rect, with_ai_rect, quit_rect]:
            # Draw black border (thicker rectangle for border)
            border_thickness = 3
            border_rect = pygame.Rect(
                rect.x - border_thickness,
                rect.y - border_thickness,
                rect.width + 2 * border_thickness,
                rect.height + 2 * border_thickness,
            )
            pygame.draw.rect(menu_win, Color.BLACK, border_rect, border_radius=15)

            # Draw white background (smaller rectangle inside border)
            pygame.draw.rect(menu_win, Color.WHITE, rect, border_radius=15)

        # Render button text and center it
        play_with_player_text = Font.NORMAL_FONT.render("Play with player", True, Color.BLACK)
        play_with_ai_text = Font.NORMAL_FONT.render("Play with AI", True, Color.BLACK)
        quit_text = Font.NORMAL_FONT.render("Quit", True, Color.BLACK)

        # get center
        menu_win.blit(play_with_player_text, (
            with_player_rect.x + (with_player_rect.width - play_with_player_text.get_width()) // 2,
            with_player_rect.y + (with_player_rect.height - play_with_player_text.get_height()) // 2
        ))
        menu_win.blit(play_with_ai_text, (
            with_ai_rect.x + (with_ai_rect.width - play_with_ai_text.get_width()) // 2,
            with_ai_rect.y + (with_ai_rect.height - play_with_ai_text.get_height()) // 2
        ))
        menu_win.blit(quit_text, (
            quit_rect.x + (quit_rect.width - quit_text.get_width()) // 2,
            quit_rect.y + (quit_rect.height - quit_text.get_height()) // 2
        ))

        # Handle events
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
