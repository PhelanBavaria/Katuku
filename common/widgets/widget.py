

import pygame


class Widget(pygame.Surface):
    def __init__(self, size):
        pygame.Surface.__init__(self, size)

    def on_click(self):
        pass

    def draw(self, surface):
        pass
