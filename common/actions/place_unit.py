

from common.actions import Action


class PlaceUnit(Action):
    subscribers = []
    def __init__(self, campaign, province, player, unit_amount=1):
        self.campaign = campaign
        self.province = province
        self.player = player
        self.unit_amount = unit_amount

    def __call__(self):
        Action.__call__(self)
        self.player.units_to_place -= self.unit_amount
        if self.province.controller != self.player:
            self.province.controller = self.player
            self.province.unit_amount = self.unit_amount
        else:
            self.province.unit_amount += self.unit_amount
