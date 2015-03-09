

from common.actions import Action


class AmassUnits(Action):
    subscribers = []
    def __init__(self, campaign, province, player, unit_amount=1):
        self.campaign = campaign
        self.province = province
        self.player = player
        self.unit_amount = unit_amount

    def __call__(self):
        if not self.useable():
            return False
        max_units = self.campaign.gamerules['max_units_province']
        self.unit_amount = min(self.unit_amount, max_units-self.province.unit_amount)
        Action.__call__(self)
        self.player.units_to_place -= self.unit_amount
        self.province.unit_amount += self.unit_amount
        return True

    def useable(self):
        max_units = self.campaign.gamerules['max_units_province']

        unit_cap = self.province.unit_amount >= max_units
        same_controller = self.province.controller == self.player
        return not unit_cap and same_controller