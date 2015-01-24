

import random
from common import util
from interfaces import Player


class AI(Player):
    def on_province_selection(self):
        pass

    def update(self):
        if self.units_to_place:
            return self.place_unit()
        else:
            return self.attack()

    def attack(self):
        province = random.choice(self.border())
        enemies = [e for e in province.neighbours if e.controller != province.controller]
        enemy = random.choice(enemies)
        return ('attack', enemy, province, province.unit_amount-1)

    def place_unit(self):
        provinces = self.game.campaign.provinces
        unoccupied = [i for i, p in provinces if not p.controller]
        if unoccupied:
            province = random.chaice(unoccupied)
        else:
            province = random.choice(self.provinces)
        return ('place_unit', province, self)

    def border(self):
        return [p for p in self.provinces if [e for e in p.neighbours if e.controller != p.controller]]

    def most_endangered_province(self):
        most_endangered = None
        for province in self.provinces:
            province = self.game.campaign.provinces[province]
            if not most_endangered:
                most_endangered = province.endangered()
            else:
                pe = province.endangered()
                if pe > most_endangered:
                    most_endangered = pe
        return most_endangered
