

import logging
from common.events import Event


class SelectProvince(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, color=None):
        filters = {
            'color': color
        }
        self.handlers.append((handler, filters))
        logging.info('Handler ' + str(handler) + 'was added to SelectProvince')

    def trigger(self, color):
        for handler, filters in self.handlers:
            is_color = filters['color'] in (color, None)
            if is_color:
                handler(color)

        logging.info('triggered SelectProvince')
        return True
