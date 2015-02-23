

import random
from common.widgets.overlays import Overlay


class Political(Overlay):
    def __init__(self, surface):
        Overlay.__init__(self, surface)
        self.unit_locations = {}

    def update(self, province, area):
        bcolor = ()
        if not province.passable:
            pcolor = (90, 90, 90)
        elif province.water:
            pcolor = (64, 64, 157)
        elif not province.controller:
            pcolor = (160, 160, 160)
        else:
            pcolor = province.controller.pcolor
            bcolor = province.controller.bcolor
        if not bcolor:
            bcolor = (255-v for v in pcolor)

        for pixel in area:
            self.surface.set_at(pixel, pcolor)

        if province.color not in self.unit_locations.keys():
            self.unit_locations[province.color] = []
        unit_dif = province.unit_amount - len(self.unit_locations[province.color])
        if unit_dif > 0:
            for u in range(unit_dif):
                pos = random.choice(area)
                self.unit_locations[province.color].append(pos)
                self.surface.set_at(pos, bcolor)
        elif unit_dif < 0:
            for u in range(abs(unit_dif)):
                pos = random.choice(self.unit_locations[province.color])
                self.unit_locations[province.color].remove(pos)
                self.surface.set_at(pos, pcolor)
