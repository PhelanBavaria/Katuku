

import pygame
from interfaces import Base


class Player(Base):
    def __init__(self, name, color, game):
        Base.__init__(self, game)
        self.name = name
        self.color = color
        self.units_to_place = 0
        self.provinces = []

    def update(self):
        campaign = self.game.campaign
        selected_province = campaign.selected_province

        if not selected_province:
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
