

from campaign.controllers import Player


class LocalPlayer(Player):
    def place_unit(self):
        if not self.country:
            self.placement_done = True
        elif not self.country.origin_province:
            return
        else:
            province = self.country.origin_province
            return self.campaign.events['amass_units'].trigger(province)

    def attack(self):
        if not self.country:
            self.attacking_done = True
        elif not self.country.goal_province:
            return
        else:
            result = self.campaign.events['attack'].trigger(self.country.origin_province, self.country.goal_province, self.country.origin_province.unit_amount)
            self.country.origin_province = None
            self.country.goal_province = None
            return result

    def on_province_selection(self, color):
        province = self.campaign.provinces[color]
        if province.controller == self.country:
            self.country.origin_province = province
        elif province == self.country.origin_province:
            self.country.origin_province = None
        elif self.country.origin_province and \
             province.color in self.country.origin_province.neighbours and \
             self.placement_done:
            self.country.goal_province = province
