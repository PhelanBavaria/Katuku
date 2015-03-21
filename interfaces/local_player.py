

from random import randint
import pygame
from interfaces import Player
from common import actions


class LocalPlayer(Player):
    def attack(self):
        action = actions.Attack(self.game.campaign, self.country.goal_province,
                                self.country.origin_province,
                                self.country.origin_province.unit_amount)
        self.country.origin_province = None
        self.country.goal_province = None
        return action

    def place_unit(self):
        return actions.AmassUnits(self.game.campaign, self.country.origin_province, self)

    def on_province_selection(self, action):
        province = self.game.campaign.provinces[action.color]
        if province.controller == self:
            self.country.origin_province = province
        elif province == self.country.origin_province:
            self.country.origin_province = None
        elif self.country.origin_province and province.color in self.country.origin_province.neighbours:
            self.country.goal_province = province
