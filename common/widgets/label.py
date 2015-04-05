

import pygame
from common.widgets import Widget


class Label(Widget):
    def __init__(self, text):
        self.norm_font = pygame.freetype.Font('gfx/fonts/CelticHand.ttf', 50)
        self.text = text

    def draw(self, surface):
        text, rect = self.norm_font.render(self.text, fgcolor=(255, 255, 255), size=30)
        rect.move_ip(self.x, self.y)
        surface.blit(text, rect)
