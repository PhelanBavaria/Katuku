

import random
from operator import itemgetter
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
            border = set()
            sorted_area = sorted(area)
            last_x, last_y = sorted_area[0]
            for x, y in sorted_area[1:]:
                if y > last_y+1 or x != last_x:
                    border.add((x, y))
                    border.add((last_x, last_y))
                last_x, last_y = x, y
            sorted_area = sorted(area, key=itemgetter(1, 0))
            last_x, last_y = sorted_area[0]
            for x, y in sorted_area[1:]:
                if x > last_x+1 or y != last_y:
                    border.add((x, y))
                    border.add((last_x, last_y))
                last_x, last_y = x, y

            self.borders[province.color] = border

        for pixel in area:
            self.surface.set_at(pixel, pcolor)
        for pixel in self.unit_locations[province.color]:
            self.surface.set_at(pixel, bcolor)
        for pixel in self.borders[province.color]:
            self.surface.set_at(pixel, bcolor)
