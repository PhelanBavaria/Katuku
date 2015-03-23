

from campaign.controllers import Player
from common import actions


class LocalPlayer(Player):
    def attack(self):
        action = actions.Attack(self.campaign, self.country.goal_province,
                                self.country.origin_province,
                                self.country.origin_province.unit_amount)
        self.country.origin_province = None
        self.country.goal_province = None
        return action

    def place_unit(self):
        return actions.AmassUnits(self.campaign, self.country.origin_province, self.country)

    def on_province_selection(self, action):
        province = self.campaign.provinces[action.color]
        if province.controller == self.country:
            self.country.origin_province = province
        elif province == self.country.origin_province:
            self.country.origin_province = None
        elif self.country.origin_province and province.color in self.country.origin_province.neighbours:
            self.country.goal_province = province
