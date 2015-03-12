

import random
from common import util
from common import actions


class Province:
    campaign = None
    controller = None
    unit_amount = 0
    passable = True
    water = False

    def __init__(self, color, campaign):
        self.color = color
        self.campaign = campaign
        self.neighbours = set()

    def __setattr__(self, name, value):
        if name == 'color':
            self.passable = True
            self.water = False
            hue = util.rgb_to_hsv(value)[0]
            if all([c == 255 for c in value[:3]]):
                self.passable = False
            elif hue >= 180 and hue <= 260:
                self.water = True
                print('water', value, hue)
        elif name == 'controller':
            if self.controller:
                self.controller.provinces.remove(self.color)
            value.provinces.append(self.color)
        object.__setattr__(self, name, value)

    def endangered(self):
        level = 0
        for province in self.neighbours:
            province = self.game.campaign.provinces[province]
            if province.controller == self.controller:
                continue
            level += province.unit_amount
        return round(level / self.unit_amount)

    def occupiable(self):
        return not self.water and self.passable and not self.controller
