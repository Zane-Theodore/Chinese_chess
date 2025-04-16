import pygame
import sys

from game.board import Board
from gui.gui import GameUI
from game.menu import Menu
from gui.menu_renderer import MenuRenderer

if __name__ == '__main__':
    pygame.init()

    # === Setup giao diện cơ bản ===
    gameUI = GameUI()
    WIDTH = gameUI.width
    HEIGHT = gameUI.height
    win = gameUI.win

    # === Khởi tạo menu và renderer ===
    menu = Menu()
    menu_renderer = MenuRenderer(win, menu)
    board = None  # Chưa tạo bàn cờ vội
    clock = pygame.time.Clock()

    mouse_pos = None
    running = True
    mode = None  # PvP, PvE hoặc None

    while running:
        pygame.time.delay(50)
        WIDTH = gameUI.width
        HEIGHT = WIDTH // 9 * 10
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if mode is None:  # Hiển thị menu
                if event.type == pygame.MOUSEMOTION:
                    menu_renderer.handle_mouse_hover(mouse_pos)

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if menu.submenu_active:
                        # Vẽ lại để lấy x_button_rect
                        x_button_rect = menu_renderer.draw_submenu()
                        if x_button_rect.collidepoint(mouse_pos):
                            menu.close_submenu()
                        else:
                            ai_idx = menu_renderer.get_ai_option_at_pos(mouse_pos)
                            if ai_idx is not None:
                                menu.ai_selected_index = ai_idx
                                mode = "pve"
                                print("Chế độ PvE được chọn với độ khó:", menu.select_option())
                                # AI modes
                    else:
                        idx =  menu_renderer.get_main_option_at_pos(mouse_pos)
                        if idx == 0:  # PvP
                            mode = "pvp"
                            board = Board(gameUI)
                        elif idx == 1:  # PvE
                            menu.open_submenu()
                        elif idx == 2:  # Quit
                            pygame.quit()
                            sys.exit()

            elif board:  # Đang trong game
                if mouse_pos[0] > WIDTH or mouse_pos[1] > HEIGHT:
                    board.picked_up_piece = None
                    continue

                if event.type == pygame.MOUSEBUTTONDOWN:
                    y, x = board.Find_Node(mouse_pos, WIDTH)
                    board.handle_mouse_down((x, y))
                elif event.type == pygame.MOUSEBUTTONUP:
                    y, x = board.Find_Node(mouse_pos, WIDTH)
                    board.handle_mouse_up((x, y))
                elif event.type == pygame.MOUSEMOTION:
                    y, x = board.Find_Node(mouse_pos, WIDTH)
                    if (
                        board.picked_up_piece
                        or (board.on_board((x, y)) and board.config[x][y] and board.config[x][y].team == board.current_turn)
                    ):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

        # === Vẽ màn hình ===
        if mode is None:
            menu_renderer.draw()
        elif board:
            if board.is_inCheck(board.current_turn) and board.isCheckMated():
                print("Check mate!! Red wins" if board.current_turn == 'b' else 'Black wins')
                pygame.quit()
                sys.exit()

            game_state = board.get_game_state()
            game_state.append(mouse_pos)
            gameUI.update_display(game_state, board)

        pygame.display.flip()
        clock.tick(60)
