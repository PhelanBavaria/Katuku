

from common import util


class Province:
    def __init__(self, campaign):
        self.campaign = campaign
        self.controller = ''
        self.inner = []
        self.neighbours = set()
        self.unit_amount = 0
        self.passable = True
        self.water = False

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'color':
            self.passable = True
            self.water = False
            if all([c <= 90 for c in value]):
                self.passable = False
            elif value[2] == 255:
                self.water = True

    def battle(self, attacker, unit_amount):
        self.campaign.add_histor('battle', {
            'province': self.color,
            'attacker': attacker.name,
            'unit_amount': unit_amount
        })
        if not self.unit_amount:
            self.unit_amount = unit_amount
            self.controller = attacker
            attacker.provinces.append(self)

    def endangered(self):
        level = 0
        for province in self.neighbours:
            province = self.game.campaign.provinces[province]
            if province.controller == self.controller:
                continue
            level += province.unit_amount
        return round(level / self.unit_amount)
