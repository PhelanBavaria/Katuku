

import pygame
from time import time
from common.util import middle
from common.widgets import Widget
from common import actions
from common.widgets.overlays import Political


class GameMap(Widget):
    def __init__(self, map_path, game):
        actions.AmassUnits.subscribers.append(self.on_place)
        actions.ChangeOwner.subscribers.append(self.on_place)
        actions.Attack.subscribers.append(self.on_attack)
        self.surface = pygame.image.load(map_path)
        Widget.__init__(self, self.surface.get_size())
        self.game = game
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
            province = self.game.campaign.provinces[color]
            self.views['political'].update(province, area)

    def on_click(self):
        pos = pygame.mouse.get_pos()
        color = tuple(self.surface.get_at(pos))
        select_province = actions.SelectProvince(self.game.campaign, color)
        select_province()

    def on_hover(self):
        pos = pygame.mouse.get_pos()
        color = tuple(self.surface.get_at(pos))
        units = self.game.campaign.provinces[color].unit_amount
        font = pygame.freetype.Font('gfx/fonts/CelticHand.ttf', 50)
        text, rect = font.render(str(units), size=15)
        area = self.province_areas[color]
        rect.move_ip(*pos)
        rect = rect.move(20, -15)
        self.hovering_over = text, rect

    def on_place(self, action):
        print('Player', action.player.name, 'placed', action.unit_amount,
              'units on', action.province.color)
        area = self.province_areas[action.province.color]
        self.views['political'].update(action.province, area)

    def on_attack(self, action):
        attacker = action.attacker.controller.name
        try:
            defender = action.defender.controller.name
        except AttributeError:
            defender = None
        if action.won:
            result = 'won'
        else:
            result = 'lost'
        print('Player', attacker,
              'attacked', action.defender_unit_amount, 'units on',
              action.defender.color, '(' + str(defender) + ')',
              'from', action.attacker.color,
              'with', action.unit_amount, 'out of',
              action.attacker.unit_amount+action.unit_amount, 'units',
              'and', result,
              '(', action.defender_dice, 'vs.', action.attacker_dice, ')')
        aarea = self.province_areas[action.attacker.color]
        darea = self.province_areas[action.defender.color]
        self.views['political'].update(action.attacker, aarea)
        self.views['political'].update(action.defender, darea)

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
        province = self.game.campaign.provinces[province_id]
        color = (255, 255, 255, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))

    def goal_overlay(self, province_id):
        province = self.game.campaign.provinces[province_id]
        color = (0, 0, 0, 125)
        for x, y in province.border:
            self.surface.fill(color, pygame.Rect(x, y, 1, 1))
