class Menu:
    def __init__(self):
        self.options = ["PvP", "PvE", "Quit"]
        self.selected_index = 0
        self.submenu_active = False
        self.ai_levels = ["Easy", "Medium", "Hard"]
        self.ai_selected_index = 0

    def move_up(self):
        if self.submenu_active:
            self.ai_selected_index = (self.ai_selected_index - 1) % len(self.ai_levels)
        else:
            self.selected_index = (self.selected_index - 1) % len(self.options)

    def move_down(self):
        if self.submenu_active:
            self.ai_selected_index = (self.ai_selected_index + 1) % len(self.ai_levels)
        else:
            self.selected_index = (self.selected_index + 1) % len(self.options)

    def select_option(self):
        if self.submenu_active:
            return self.ai_levels[self.ai_selected_index]
        else:
            return self.options[self.selected_index]

    def open_submenu(self):
        self.submenu_active = True
        self.ai_selected_index = 0

    def close_submenu(self):
        self.submenu_active = False
