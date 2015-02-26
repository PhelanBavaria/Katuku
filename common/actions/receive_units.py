

import random
from common.actions import Action
from common.actions import PlaceUnit


class ReceiveUnits(Action):
    subscribers = []
    def __init__(self, campaign, player):
        self.campaign = campaign
        self.player = player
        self.province_units = 0
        self.extra_units = 0

    def extra(self, units):
        self.extra_units += units

    def place_randomly(self):
        amount = self.player.units_to_place
        provinces = list(self.campaign.provinces.values())
        unoccupied = [p for p in provinces if p.occupiable()]
        for unit in range(amount):
            if unoccupied:
                province = random.choice(unoccupied)
                unoccupied.remove(province)
            else:
                color = random.choice(self.player.provinces)
                province = self.campaign.provinces[color]
            PlaceUnit(self.campaign, province, self.player)()

    def __call__(self):
        province_units = self.campaign.gamerules['new_units_per_turn']
        if callable(province_units):
            self.province_units = province_units(self.campaign, self.player)
        else:
            self.province_units = province_units
        Action.__call__(self)
        self.player.units_to_place += self.province_units
        self.player.units_to_place += self.extra_units
        self.province_units = 0
        self.extra_units = 0
        if self.campaign.gamerules['auto_unit_placement']:
            self.place_randomly()
