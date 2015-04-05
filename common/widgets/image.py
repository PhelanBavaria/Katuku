

import pygame
from common.widgets import Widget


class Image(Widget):
    def __init__(self, image):
        self.image = image
        self.resize(self.w, self.h)

    def draw(self, surface):
        surface.blit(self.image, (self.x, self.y))

    def resize(self, w, h):
        Widget.resize(self, w, h)
        print(1)
        self.image = pygame.transform.scale(self.image, (w, h))
