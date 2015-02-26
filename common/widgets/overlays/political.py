

import random
from common import util
from common.widgets.overlays import Overlay


class Political(Overlay):
    def __init__(self, surface):
        Overlay.__init__(self, surface)
        self.unit_locations = {}
        self.borders = {}

    def update(self, province, area):
        bcolor = ()
        if not province.passable:
            pcolor = (90, 90, 90)
        elif province.water:
            pcolor = (64, 64, 157)
            bcolor = (100, 100, 157)
        elif not province.controller:
            pcolor = (160, 160, 160)
        else:
            pcolor = province.controller.pcolor
            bcolor = province.controller.bcolor
        if not bcolor:
            bcolor = tuple(255-v for v in pcolor)

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
            self.surface.set_at(pixel, pcolor)
        for pixel in self.unit_locations[province.color]:
            self.surface.set_at(pixel, bcolor)
        for pixel in self.borders[province.color]:
            self.surface.set_at(pixel, bcolor)
