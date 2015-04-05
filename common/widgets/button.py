

import pygame
from common.widgets import Widget



class Button(Widget):
    w = 50
    h = 30

    def __init__(self, command):
        self.img_up = pygame.image.load('gfx/widgets/background.jpg')
        self.img_down = pygame.image.load('gfx/widgets/background_pressed.jpg')
        self.clicked = False
        self.command = command
        self.resize(self.w, self.h)

    def on_click(self):
        self.command()

    def draw(self, surface):
        if self.clicked:
            surface.blit(self.img_down, (self.x, self.y))
        else:
            surface.blit(self.img_up, (self.x, self.y))

    def resize(self, w, h):
        Widget.resize(self, w, h)
        self.img_up = pygame.transform.scale(self.img_up, (w, h))
        self.img_down = pygame.transform.scale(self.img_down, (w, h))
