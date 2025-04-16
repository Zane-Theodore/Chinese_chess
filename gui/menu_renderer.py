import pygame
from utils.config import Color, Font, WIDTH, HEIGHT

class MenuRenderer:
    def __init__(self, screen, menu):
        self.screen = screen
        self.menu = menu
        self.main_option_rects = []
        self.ai_option_rects = []

    def draw_main_menu(self):
        self.screen.fill(Color.GRAY)
        self.main_option_rects = []

        title_text = Font.TITTLE_FONT.render("CHINESE CHESS", True, Color.WHITE)
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = HEIGHT // 6 - title_text.get_height() // 2
        self.screen.blit(title_text, (title_x, title_y))

        spacing = HEIGHT // 12
        start_y = int(HEIGHT * 0.4)

        for i, option in enumerate(self.menu.options):
            color = Color.YELLOW if i == self.menu.selected_index else Color.WHITE
            text_surface = Font.NORMAL_FONT.render(option, True, color)
            x = WIDTH // 2 - text_surface.get_width() // 2
            y = start_y + i * spacing
            rect = self.screen.blit(text_surface, (x, y))
            self.main_option_rects.append((rect, i))

    def draw_submenu(self):
        self.ai_option_rects = []

        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((255, 255, 255, 30)) 
        self.screen.blit(overlay, (0, 0))

        # Create the frame
        box_width = WIDTH // 2
        box_height = HEIGHT // 2
        box_x = (WIDTH - box_width) // 2
        box_y = (HEIGHT - box_height) // 2

        box_rect = pygame.Rect(box_x, box_y, box_width, box_height)
        pygame.draw.rect(self.screen, Color.GRAY, box_rect)
        pygame.draw.rect(self.screen, Color.WHITE, box_rect, 2)

        # X button
        x_button_size = 40
        x_button_rect = pygame.Rect(box_x + box_width - x_button_size - 10, box_y + 10, x_button_size, x_button_size)
        pygame.draw.rect(self.screen, Color.RED, x_button_rect)
        x_text =Font.NORMAL_FONT.render("X", True, Color.WHITE)
        x_text_rect = x_text.get_rect(center=x_button_rect.center)
        self.screen.blit(x_text, x_text_rect)

        # Align all options evenly in the submenu
        num_options = len(self.menu.ai_levels)
        spacing = box_height // (num_options + 1)

        for i, level in enumerate(self.menu.ai_levels):
            color = Color.YELLOW if i == self.menu.ai_selected_index else Color.WHITE
            text_surface = Font.NORMAL_FONT.render(level, True, color)
            x = box_x + box_width // 2 - text_surface.get_width() // 2
            y = box_y + spacing * (i + 1) - text_surface.get_height() // 2
            rect = self.screen.blit(text_surface, (x, y))
            self.ai_option_rects.append((rect, i))

        return x_button_rect

    def draw(self):
        if self.menu.submenu_active:
            return self.draw_submenu()
        else:
            self.draw_main_menu()
            return None

    def handle_mouse_hover(self, pos):
        if self.menu.submenu_active:
            for rect, idx in self.ai_option_rects:
                if rect.collidepoint(pos):
                    self.menu.ai_selected_index = idx
                    break
        else:
            for rect, idx in self.main_option_rects:
                if rect.collidepoint(pos):
                    self.menu.selected_index = idx
                    break

    def get_main_option_at_pos(self, pos):
        for rect, idx in self.main_option_rects:
            if rect.collidepoint(pos):
                return idx
        return None

    def get_ai_option_at_pos(self, pos):
        for rect, idx in self.ai_option_rects:
            if rect.collidepoint(pos):
                return idx
        return None
