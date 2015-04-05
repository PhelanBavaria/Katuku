

from common.widgets import Widget


class Toggler(Widget):
    def __init__(self):
        self.img_true = None
        self.img_false = None
        self.state = False

    def on_click(self):
        self.state = not self.state

    def draw(self, surface):
        if self.state:
            surface.blit(self.img_true)
        else:
            surface.blit(self.img_false)
