

import pygame


class Overlay(pygame.Surface):
    def __init__(self):
        pygame.Surface.__init__(self, 0, 0)
        self.pos = ()
        self.width = 0
        self.height = 0

    def insert(self, pos, color):
        if not self.pos:
            self.pos = pos
            self.set_at(pos, color)
        elif pos[0] < self.pos[0]:
            self.width += self.pos[0] - pos[0]
            self.pos[0] = self.pos[0]
        elif pos[1] < self.pos[1]:
            self.height += self.pos[1] - pos[1]
            self.pos[1] = self.pos[1]
        elif pos[0] - self.pos[0] > self.width:
            self.width = pos[0] - self.pos[0]
        elif pos[1] - self.pos[1] > self.height:
            self.height = pos[1] - self.pos[1]
        else:
            self.set_at(pos, color)
        self.
        self.set_at(pos, color)
