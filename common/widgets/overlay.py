

from common.widgets import Widget


class Overlay(Widget):
    def __init__(self, surface, pixels, color):
        x, y = pixels[0]
        mx, my = 0, 0
        for pixel in pixels[1:]:
            if pixel[0] < x:
                x = pixel[0]
            if pixel[1] < y:
                y = pixel[0]
            if pixel[0] > mx:
                mx = pixel[0]
            if pixel[1] > my:
                my = pixel[0]
            width, height = mx-x, my-y
        Widget.__init__(surface, x, y, width, height)
        self.add_layer(pixels, color)

    def add_layer(self, pixels, color):
        for y in range(self.height):
            for x in range(self.width):
                if (x, y) in pixels:
                    self.set_at((x, y), color)

