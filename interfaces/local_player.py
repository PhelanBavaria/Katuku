

from random import randint
import pygame
from interfaces import Player
from common import actions


class LocalPlayer(Player):
    def make_decision(self):
        campaign = self.game.campaign

        if not self.origin_province:
            self.goal_province = None
        elif self.units_to_place > 0:
            return self.place_unit()
        elif self.goal_province:
            return self.attack()

    def attack(self):
        action = actions.Attack(self.game.campaign, self.goal_province,
                                self.origin_province,
                                self.origin_province.unit_amount)
        self.origin_province = None
        self.goal_province = None
        return action

    def place_unit(self):
        return actions.AmassUnits(self.game.campaign, self.origin_province, self)

    def on_province_selection(self, action):
        province = self.game.campaign.provinces[action.color]
        print('Selected province:', action.color,
              '\nController:', province.controller,
              '\nUnits:', province.unit_amount)
        if province.controller == self:
            self.origin_province = province
        elif province == self.origin_province:
            self.origin_province = None
        elif self.origin_province and province.color in self.origin_province.neighbours:
            self.goal_province = province

    def bordering_provinces(self):
        for province in self.provinces:
            for neighbour in province.neighbours:
                if neighbour not in self.provinces:
                    yield neighbour
