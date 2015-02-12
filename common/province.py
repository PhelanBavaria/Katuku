

import random
from common import util
from common import actions


class Province:
    color = ()
    campaign = None
    controller = None
    inner = []
    neighbours = set()
    unit_amount = 0
    passable = True
    water = False

    def __init__(self, color, campaign):
        self.color = color
        self.campaign = campaign

    def __setattr__(self, name, value):
        if name == 'color':
            self.passable = True
            self.water = False
            if all([c <= 90 for c in value]):
                self.passable = False
            elif value[2] == 255:
                self.water = True
        elif name == 'controller':
            if self.controller:
                self.controller.provinces.remove(self.color)
            value.provinces.append(self.color)
        if self.color == (48, 118, 56, 255) and name == 'unit_amount':
        object.__setattr__(self, name, value)

    def endangered(self):
        level = 0
        for province in self.neighbours:
            province = self.game.campaign.provinces[province]
            if province.controller == self.controller:
                continue
            level += province.unit_amount
        return round(level / self.unit_amount)

    def occupiable(self, occupant):
        # if not self.controller:
        #     print(self.color, self.water, self.passable, self.controller)
        #     print(not self.water and self.passable and not self.controller)
        return not self.water and self.passable and not self.controller
