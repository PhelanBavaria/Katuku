

import pygame
from time import time
from common.widgets import Widget


class GameMap(Widget):
    def __init__(self, surface, x, y, width, height, game):
        Widget.__init__(self, surface, x, y, width, height)
        self.game = game
        self.overlays = {
            'faction_overlay': [
                self.faction_overlay(),
                self.unit_overlay()
            ]
        self.current_overlay = 'faction_overlay'
        self.last_draw = round(time(), 2)
        self.last_turn = 0

    def on_click(self):
        pos = pygame.mouse.get_pos()
        color = self.game.campaign.prov_map.get_at(pos)
        color = '#%02x%02x%02x' % color[0:3]
        print('Clicked on province', color)
        self.game.campaign.selected_province = color

    def draw(self):
        Widget.draw(self)
        if time() - self.last_draw < 1.0:
            return
        
        self.last_draw = time()
        if campaign.turn > self.last_turn:
            for t in range(self.last_turn+1, campaign.turn+1):
                history = campaign.history[t]
                try:
                    battles = history['battle']
                except KeyError:
                    continue
                for battle in battles:
                    province = campaign.provinces[battle['province']]
                    overlay = self.overlays['faction_overlay']
                    p_color = province.controller.color
                    r, g, b = p_color
                    b_color = 255-r, 255-g, 255-b
                    overlay.add_layer(province.pixels, p_color)
                    overlay.add_layer(province.border, b_color)
            self.last_turn = campaign.turn
        #self.surface.blit(self.game.campaign.prov_map, (self.x, self.y))
        # for _id, province in self.game.campaign.provinces.items():
        #     if _id not in self.provinces:
        #         self.provinces[_id] = [
        #             self.player_color_overlay(province),
        #             self.border_overlay(province),
        #             self.unit_overlay(province)
        #         ]
        #     for overlay in self.provinces[_id]:
        #         for coord, color in overlay.items():
        #             rect = pygame.Rect(coord, (1, 1))
        #             self.surface.fill(color, rect)
        # province_id = self.game.campaign.origin_province
        # if province_id:
        #     self.origin_overlay(province_id)
        # province_id = self.game.campaign.goal_province
        # if province_id:
        #     self.goal_overlay(province_id)

    def player_color_overlay(self, province):
        for pixel in province.pixels:
            try:
                color = province.controller.color
            except AttributeError:
                color = (200, 200, 200)
            overlay[pixel] = color
        return overlay   

    def border_overlay(self, province):
        overlay = {}
        for pixel in province.border:
            try:
                r, g, b = province.controller.color
                color = 255-r, 255-g, 255-b
            except AttributeError:
                color = (55, 55, 55)
            overlay[pixel] = color
        return overlay

    def unit_overlay(self, province):
        overlay = {}
        for pixel in province.pixels:
            color = (255, 255, 255, 100)
            overlay[pixel] = color
        return overlay

    def origin_overlay(self, province_id):
        province = self.game.campaign.provinces[province_id]
        color = (255, 255, 255, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))

    def goal_overlay(self, province_id):
        province = self.game.campaign.provinces[province_id]
        color = (0, 0, 0, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))
