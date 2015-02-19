

import os
import pygame
from time import time
from common.widgets import Widget
from common import actions


class GameMap(Widget):
    def __init__(self, pos, size, game, players):
        Widget.__init__(self, pos, size)
        actions.PlaceUnit.subscribers.append(self.on_place)
        actions.Attack.subscribers.append(self.on_attack)
        self.game = game
        self.players = players
        self.provinces = {}
        self.map_pos = (0, 0)
        self.zoom = 1
        self.view = 'political'
        self.views = {}
        self.overlays = {}
        file_name = game.campaign.map_name + '.bmp'
        surface = pygame.image.load(os.path.join('content', 'maps', file_name))
        self.views['political'] = surface
        width, height = surface.get_width(), surface.get_height()
        for y in range(height):
            for x in range(width):
                color = tuple(surface.get_at((x, y)))
                if color not in self.provinces.keys():
                    self.provinces[color] = []
                self.provinces[color].append((x, y))
        for color in game.campaign.provinces.keys():
            self.update_political(color)

    def on_click(self):
        pos = pygame.mouse.get_pos()
        color = self.game.campaign.prov_map.get_at(pos)
        print('Clicked on province', color)
        self.game.campaign.selected_province = color

    def on_place(self, action):
        pygame.time.wait(1000)
        self.update_political(action.province.color)

    def on_attack(self, action):
        pygame.time.wait(1000)
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
        if action.won:
            self.update_political(action.defender.color)

    def draw(self, surface):
        surface.blit(self.views[self.view], self.pos)

    def update_political(self, color):
        province = self.game.campaign.provinces[color]
        for pixel in self.provinces[color]:
            bcolor = ()
            if not province.passable:
                pcolor = (90, 90, 90)
            elif province.water:
                pcolor = (64, 64, 157)
            elif not province.controller:
                pcolor = (160, 160, 160)
            else:
                pname = province.controller.name
                pcolor = self.players[pname][0]
                bcolor = self.players[pname][1]
            if not bcolor:
                bcolor = (255-v for v in pcolor)
            self.views['political'].set_at(pixel, pcolor)

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
