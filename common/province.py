

from common import util


class Province:
    def __init__(self, campaign, color):
        self.campaign = campaign
        self.color = color
        self.controller = None
        self.pixels = []
        self.border = []
        self.neighbours = set()
        self.center = (0, 0)
        self.unit_amount = 0

    def __setattr__(self, name, value):
        object.__setattr__(self, name, value)
        if name == 'border':
            if not self.border:
                self.center = value
                return
            x, y = 0, 0
            for coord in self.border:
                x += coord[0]
                y += coord[1]
            x /= len(self.border)
            y /= len(self.border)
            self.center = (x, y)

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
