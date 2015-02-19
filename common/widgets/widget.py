

import pygame


class Widget(pygame.Surface):
    def __init__(self, pos, size):
        self.pos = pos
        self.size = size

    def on_click(self):
        pass

    def draw(self, surface):
        pass
