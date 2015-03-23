

import random
from campaign.controllers import Player
from common import actions


class AI(Player):
    def on_province_selection(self, action):
        pass

    def make_decision(self):
        if not self.country:
            return
        elif self.country.units_to_place:
            return self.place_unit()
        else:
            return self.attack()

    def attack(self):
        battles = self.possible_battles()
        if not battles:
            self.ready = True
            return
        battle = random.choice(battles)
        province = battle[1]
        enemy_prov = battle[2]
        return actions.Attack(self.campaign, enemy_prov, province,
                              province.unit_amount-1)

    def place_unit(self):
        province = random.choice(self.country.provinces)
        province = self.campaign.provinces[province]
        return actions.AmassUnits(self.campaign, province, self.country)

    def possible_battles(self):
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
                ap = ps[p].unit_amount-1
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
