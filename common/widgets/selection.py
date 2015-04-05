

from common.widgets import Widget


class Selection(Widget):
    def __init__(self, items):
        self.img_selection = None
        self.img_dropdown = None
        self.clicked = False
        self.items = items

    def on_click(self):
        self.clicked = True

    def draw(self, surface):
        surface.blit(self.img_selection)
        if self.clicked:
            surface.blit(self.img_dropdown)
