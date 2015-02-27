

from common.actions import Action


class PlaceUnit(Action):
    subscribers = []
    def __init__(self, campaign, province, player, unit_amount=1):
        self.campaign = campaign
        self.province = province
        self.player = player
        self.unit_amount = unit_amount

    def __call__(self):
        if not self.useable():
            print('not useable')
            return
        max_units = self.campaign.gamerules['max_units_province']
        self.unit_amount = min(self.unit_amount, max_units-self.province.unit_amount)
        Action.__call__(self)
        self.player.units_to_place -= self.unit_amount
        if self.province.controller != self.player:
            self.province.controller = self.player
            self.province.unit_amount = self.unit_amount
        else:
            self.province.unit_amount += self.unit_amount

    def useable(self):
        max_units = self.campaign.gamerules['max_units_province']

        not_unit_cap = self.province.unit_amount < max_units
        same_controller = self.province.controller == self.player
        no_controller = self.province.controller == None
        return not_unit_cap and same_controller or no_controller
