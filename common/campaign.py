

import os
import random
from pygame import image
from common import util
from common import actions
from common import Province
from interfaces import player_types


class Campaign:
    def __init__(self, setup):
        self.setup = setup
        self.paused = False
        self.current_player = 0
        self.map_name = ''
        self.players = [player_types[p](n, g, c1, c2) for p, n, g, c1, c2
                        in setup['players']]
        self.gamerules = setup['rules']
        self.provinces = {}

    def create(self):
        self.load_map(self.setup['map'])
        units = self.gamerules['start_units']*len(self.provinces)//len(self.players)
        for player in self.players:
            player.units_to_place = units
        if self.gamerules['auto_unit_placement']:
            provinces = list(self.provinces.values())
            while provinces:
                for player in self.players:
                    if not provinces:
                        break
                    province = random.choice(provinces)
                    actions.ChangeOwner(province, player)()
                    actions.AmassUnits(self, province, player)()
                    provinces.remove(province)

    def update(self):
        if self.current_player == len(self.players):
            self.current_player = 0
            for player in self.players:
                player.ready = False
            print('End Turn')
        elif self.players[self.current_player].ready:
            print('Player', self.players[self.current_player].name, 'ready')
            actions.ReceiveUnits(self, self.players[self.current_player])()
            self.current_player += 1
        else:
            decision = self.players[self.current_player].make_decision()
            if decision:
                decision()

    def place_random_units(self, player):
        while player.units_to_place:
            units = random.randint(1, player.units_to_place-1)
            color = random.choice(player.provinces)
            province = self.provinces[color]
            actions.AmassUnits(self, province, player, units)()

    def load_map(self, name):
        file_name = name + '.bmp'
        print('Loading map:', file_name)
        self.map_name = name
        surface = image.load(os.path.join('content', 'maps', file_name))
        width, height = surface.get_width(), surface.get_height()
        # Scanning the map from left to right, top to bottom first
        for y in range(height):
            last_color = None
            for x in range(width):
                color = tuple(surface.get_at((x, y)))  # color in RGBA
                if color not in self.provinces.keys():
                    self.provinces[color] = Province(color, self)
                if not last_color:
                    last_color = color
                elif last_color != color:
                    self.provinces[color].neighbours.add(last_color)
                    self.provinces[last_color].neighbours.add(color)
                    last_color = color
        # Scanning the map from top to bottom, left to right
        for x in range(width):
            last_color = None
            for y in range(height):
                color = tuple(surface.get_at((x, y)))
                if not last_color:
                    last_color = color
                    continue
                if last_color != color:
                    self.provinces[color].neighbours.add(last_color)
                    self.provinces[last_color].neighbours.add(color)
                    last_color = color

        # Note: Scanning twice to get directly adjacent pixels
