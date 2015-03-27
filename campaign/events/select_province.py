

from common.events import Event


class SelectProvince(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, color=None):
        filters = {
            'color': color
        }
        self.handlers.add((handler, filters))

    def trigger(self, color):
        for handler, filters in self.handlers:
            is_color = filters['color'] in (color, None)
            if is_color:
                handler()

        return True
