

import random
from common import util
from common.widgets.overlays import Overlay


class Political(Overlay):
    def __init__(self, surface):
        Overlay.__init__(self, surface)
        self.unit_locations = {}
        self.borders = {}

    def update(self, province, area):
        sec_color = ()
        if not province.passable:
            prim_color = (90, 90, 90)
        elif province.water:
            prim_color = (64, 64, 157)
            sec_color = (100, 100, 157)
        elif not province.controller:
            prim_color = (160, 160, 160)
        else:
            prim_color = province.controller.prim_color
            sec_color = province.controller.sec_color
        if not sec_color:
            sec_color = tuple(255-v for v in prim_color)

        if province.color not in self.unit_locations.keys():
            self.unit_locations[province.color] = []
        unit_dif = province.unit_amount - len(self.unit_locations[province.color])
        if unit_dif > 0:
            for u in range(unit_dif):
                pos = random.choice(area)
                self.unit_locations[province.color].append(pos)
        elif unit_dif < 0:
            for u in range(abs(unit_dif)):
                pos = random.choice(self.unit_locations[province.color])
                self.unit_locations[province.color].remove(pos)

        if province.color not in self.borders.keys():
            self.borders[province.color] = util.border(area)

        for pixel in area:
            self.surface.set_at(pixel, prim_color)
        for pixel in self.unit_locations[province.color]:
            self.surface.set_at(pixel, sec_color)
        for pixel in self.borders[province.color]:
            self.surface.set_at(pixel, sec_color)
