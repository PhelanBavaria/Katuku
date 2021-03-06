

import random
from campaign.controllers import Player


class AI(Player):
    def on_province_selection(self, color):
        pass

    def place_unit(self):
        if not self.country or self.country.units_to_place <= 0 or \
           self.unfull_provinces():
            self.placement_done = True
        else:
            province = random.choice(self.country.provinces)
            province = self.campaign.provinces[province]
            return self.campaign.events['amass_units'].trigger(province)

    def attack(self):
        if not self.country:
            self.attacking_done = True
        else:
            battles = self.possible_battles()
            if not battles:
                self.attacking_done = True
                return
            battle = random.choice(battles)
            province = battle[1]
            enemy_prov = battle[2]
            min_units_province = self.campaign.gamerules['min_units_province']
            return self.campaign.events['attack'].trigger(province, enemy_prov,
                                  province.unit_amount-min_units_province)

    def possible_battles(self):
        min_units_province = self.campaign.gamerules['min_units_province']
        ps = self.campaign.provinces
        battles = []
        for p in self.country.provinces:
            if ps[p].unit_amount < 2:
                continue
            for n in ps[p].neighbours:
                if ps[n].controller == ps[p].controller:
                    continue
                elif not ps[n].passable:
                    continue
                elif ps[n].water:
                    continue
                ap = ps[p].unit_amount-min_units_province
                dp = ps[n].unit_amount
                sr = ap - dp
                battles.append((sr, ps[p], ps[n]))
        #battles.sort()
        return battles

    def neighbours(self):
        ps = self.campaign.provinces
        result = set()
        for p in self.provinces:
            for n in ps[p].neighbours:
                if ps[n].occupiable:
                    result.add(n)
        return result

    def border(self):
        ps = self.campaign.provinces
        return [p for p in self.provinces if
            [e for e in ps[p].neighbours if
                ps[e].occupiable()]]

    def most_endangered_province(self):
        most_endangered = None
        for province in self.provinces:
            province = self.campaign.provinces[province]
            if not most_endangered:
                most_endangered = province.endangered()
            else:
                pe = province.endangered()
                if pe > most_endangered:
                    most_endangered = pe
        return most_endangered
