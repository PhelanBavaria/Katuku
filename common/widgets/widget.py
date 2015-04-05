

import pygame



class Widget:
    x = 0
    y = 0
    w = 0
    h = 0

    def on_click(self):
        pass

    def off_click(self):
        pass

    def hover(self):
        pass

    def draw(self, surface):
        pass

    def resize(self, w, h):
        self.w, self.h = w, h

    def in_bounds(self, point):
        x, y = point
        return x >= self.x and x <= self.x + self.w and \
               y >= self.y and y <= self.y + self.h
