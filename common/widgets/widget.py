

import pygame


class Widget(pygame.Surface):
    def __init__(self, surface, x, y, width, height):
        pygame.Surface.__init__(self, (width, height))
        self.surface = surface
        self.x, self.y = x, y
        self.subwidgets = []

    def on_click(self):
        pass

    def draw(self):
        self.surface.blit(self, (self.x, self.y))
        for widget in self.subwidgets:
            widget.draw()
