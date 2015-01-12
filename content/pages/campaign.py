

import pygame
from common.widgets import GameMap


class Campaign:
    def __init__(self, gui):
        self.background = pygame.Surface(gui.screen.get_size())
        self.background = self.background.convert()
        self.widgets = [
            GameMap(gui.screen, 0, 0, 800, 800, gui.game)
        ]
        self.selected_widget = None
        self.background.fill((250, 250, 250))
        gui.screen.blit(self.background, (0, 0))

    def draw(self):
        for widget in self.widgets:
            widget.draw()
