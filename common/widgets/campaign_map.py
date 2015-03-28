

import pygame
from time import time
from common.util import middle
from common.widgets import Widget
from common import events
from common.widgets.overlays import Political


class CampaignMap(Widget):
    def __init__(self, map_path, campaign):
        campaign.events['change_owner'].on_trigger(self.on_place)
        campaign.events['amass_units'].on_trigger(self.on_place)
        campaign.events['attack'].on_trigger(self.on_attack)
        self.surface = pygame.image.load(map_path)
        Widget.__init__(self, self.surface.get_size())
        self.campaign = campaign
        self.map_pos = (0, 0)
        self.zoom = 1
        self.province_areas = {}
        self.view = 'political'
        self.views = {
            'political': Political(self.surface)
        }
        self.hovering_over = None
        width, height = self.surface.get_width(), self.surface.get_height()
        for y in range(height):
            for x in range(width):
                color = tuple(self.surface.get_at((x, y)))
                if color not in self.province_areas.keys():
                    self.province_areas[color] = []
                self.province_areas[color].append((x, y))
        for color, area in self.province_areas.items():
            province = self.campaign.provinces[color]
            self.views['political'].update(province, area)

    def on_click(self):
        pos = pygame.mouse.get_pos()
        color = tuple(self.surface.get_at(pos))
        self.campaign.events['select_province'].trigger(color)

    def on_hover(self):
        pos = pygame.mouse.get_pos()
        color = tuple(self.surface.get_at(pos))
        units = self.campaign.provinces[color].unit_amount
        font = pygame.freetype.Font('gfx/fonts/CelticHand.ttf', 50)
        text, rect = font.render(str(units), size=15)
        area = self.province_areas[color]
        rect.move_ip(*pos)
        rect = rect.move(20, -15)
        self.hovering_over = text, rect

    def on_place(self, province):
        # print('Player', action.country.name, 'placed', action.unit_amount,
        #       'units on', action.province.color, action.country.units_to_place, 'left')
        area = self.province_areas[province.color]
        self.views['political'].update(province, area)

    def on_attack(self, attacker, defender, unit_amount, winner):
        # att_name = attacker.controller.name
        # try:
        #     def_name = defender.controller.name
        # except AttributeError:
        #     def_name = None
        # print('Player', att_name,
        #       'attacked', defender.unit_amount, 'units on',
        #       defender.color, '(' + str(def_name) + ')',
        #       'from', attacker.color,
        #       'with', unit_amount, 'out of',
        #       attacker.unit_amount+unit_amount, 'units',
        #       'and', winner,
        #       '(', defender_dice, 'vs.', attacker_dice, ')')
        aarea = self.province_areas[attacker.color]
        darea = self.province_areas[defender.color]
        self.views['political'].update(attacker, aarea)
        self.views['political'].update(defender, darea)

    def draw(self, surface):
        surface.blit(self.views[self.view].surface, (0, 0))
        if self.hovering_over:
            text, rect = self.hovering_over
            surface.blit(text, rect)

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

    def origin_overlay(self, province_id):
        province = self.campaign.provinces[province_id]
        color = (255, 255, 255, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))

    def goal_overlay(self, province_id):
        province = self.campaign.provinces[province_id]
        color = (0, 0, 0, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))
