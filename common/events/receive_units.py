

import random
from common.events import Event
from common.events import AmassUnits


class ReceiveUnits(Event):
    subscribers = []
    def __init__(self, campaign, country):
        self.campaign = campaign
        self.country = country
        self.province_units = 0
        self.extra_units = 0

    def extra(self, units):
        self.extra_units += units

    def __call__(self):
        province_units = self.campaign.gamerules['new_units_per_turn']
        if callable(province_units):
            self.province_units = province_units(self.campaign, self.country)
        else:
            self.province_units = province_units
        #Event.__call__(self)
        self.country.units_to_place += self.province_units
        self.country.units_to_place += self.extra_units
        self.province_units = 0
        self.extra_units = 0
