

import pygame
from time import time
from common.widgets import Widget


class GameMap(Widget):
    def __init__(self, surface, x, y, width, height, game):
        Widget.__init__(self, surface, x, y, width, height)
        self.game = game
        self.overlay = 'political'
        self.overlays = {
            'political': self.draw_political
        }
        self.current_overlay = 'political'
        self.last_draw = round(time(), 2)
        self.last_turn = 0

    def on_click(self):
        pos = pygame.mouse.get_pos()
        color = self.game.campaign.prov_map.get_at(pos)
        print('Clicked on province', color)
        self.game.campaign.selected_province = color

    def draw(self):
        Widget.draw(self)
        if time() - self.last_draw < 1.0:
            return
        self.last_draw = time()

        if self.overlay:
            self.overlays[self.overlay]()

    def draw_political(self):
        for province in self.game.campaign.provinces.values():
            if not province.passable:
                pcolor = (90, 90, 90)
                bcolor = (90, 90, 90)
            elif province.water:
                pcolor = (64, 64, 157)
                bcolor = (64, 64, 157)
            elif not province.controller:
                pcolor = (160, 160, 160)
                bcolor = (160, 160, 160)
            else:
                pcolor = province.controller.color
                bcolor = (255-v for v in pcolor)
            pygame.draw.polygon(self.surface, pcolor, province.border)
            pygame.draw.polygon(self.surface, bcolor, province.border, 1) 

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
