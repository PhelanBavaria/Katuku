

from random import randint
import pygame
from interfaces import Base
from common import actions


class Player(Base):
    def __init__(self, name, game, country=None):
        Base.__init__(self, game)
        self.name = name
        self.country = country
        self.ready = False
        actions.SelectProvince.subscribers.append(self.on_province_selection)

    def make_decision(self):
        if not self.country:
            return

        campaign = self.game.campaign

        if not self.country.origin_province:
            self.country.goal_province = None
        elif self.country.units_to_place > 0:
            return self.place_unit()
        elif self.country.goal_province:
            return self.attack()

    def attack(self):
        pass

    def place_unit(self):
        pass

    def on_province_selection(self, action):
        pass

    def bordering_provinces(self):
        for province in self.provinces:
            for neighbour in province.neighbours:
                if neighbour not in self.provinces:
                    yield neighbour
