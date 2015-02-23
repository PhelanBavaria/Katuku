

from random import randint
import pygame
from interfaces import Base
from common import actions


class Player(Base):
    def __init__(self, name, game):
        Base.__init__(self, game)
        self.name = name
        self.pcolor = tuple(randint(0, 255) for i in range(3))
        self.bcolor = tuple(randint(0, 255) for i in range(3))
        print(self.pcolor, self.bcolor)
        self.ready = False
        self.units_to_place = 0
        self.provinces = []
        self.origin_province = ()
        self.goal_province = ()
        actions.SelectProvince.subscribers.append(self.on_province_selection)

    def on_province_selection(self, action):
        province = args[0]
        if province in self.provinces:
            self.origin_province = province
        elif self.origin_province:
            origin_province = self.game.campaign.provinces[self.origin_province]
            if province in origin_province.neighbours:
                self.goal_province = province

    def bordering_provinces(self):
        for province in self.provinces:
            for neighbour in province.neighbours:
                if neighbour not in self.provinces:
                    yield neighbour

    def update(self):
        campaign = self.game.campaign

        if not self.origin_province:
            return
        elif not self.goal_province:
            return

        if self.units_to_place:
            campaign.origin_province = selected_province
            province = campaign.provinces[selected_province]
            self.units_to_place -= 1
            province.battle(self, 1)
            self.game.campaign.end_turn()
            return

        if selected_province in self.provinces:
            campaign.origin_province = selected_province
        elif campaign.origin_province:
            origin_province = campaign.provinces[campaign.origin_province]
            if selected_province in origin_province.neighbours:
                campaign.goal_province = selected_province
