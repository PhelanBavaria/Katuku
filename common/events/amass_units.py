

from common.events import Event


class AmassUnits(Event):
    subscribers = []
    def __init__(self, campaign, province, country, unit_amount=1):
        self.campaign = campaign
        self.province = province
        self.country = country
        self.unit_amount = unit_amount

    def __call__(self):
        if not self.useable():
            return False
        max_units = self.campaign.gamerules['max_units_province']
        self.unit_amount = min(self.unit_amount, max_units-self.province.unit_amount)
        #Event.__call__(self)
        self.country.units_to_place -= self.unit_amount
        self.province.unit_amount += self.unit_amount
        return True

    def useable(self):
        max_units = self.campaign.gamerules['max_units_province']

        unit_cap = self.province.unit_amount >= max_units
        same_controller = self.province.controller == self.country
        return not unit_cap and same_controller
