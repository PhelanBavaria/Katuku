

import os
import random
from pygame import image
from common import util
from common import actions
from common import Province


class Campaign:
    def __init__(self, setup):
        self.setup = setup
        self.paused = False
        self.current_player = 0
        self.map_name = ''
        self.players = setup['players']
        self.gamerules = setup['rules']
        self.provinces = {}

    def create(self):
        self.load_map(self.setup['map'])
        units = self.gamerules['start_units']*len(self.provinces)//len(self.players)
        if self.gamerules['auto_unit_placement']:
            provinces = list(self.provinces.values())
            placing_players = self.players[:]
            while placing_players:
                for player in placing_players:
                    unoccupied = [p for p in provinces if p.occupiable()]
                    if unoccupied:
                        province = random.choice(unoccupied)
                    else:
                        province = random.choice(player.provinces)
                        province = self.provinces[province]
                    actions.PlaceUnit(self, province, player)()
                if not units:
                    break
                else:
                    units -= 1

    def update(self):
        if self.current_player == len(self.players):
            self.current_player = 0
            for player in self.players:
                player.ready = False
            print('End Turn')
        elif self.players[self.current_player].ready:
            actions.ReceiveUnits(self, self.players[self.current_player])()
            print('Player', self.players[self.current_player].name, 'ready')
            self.current_player += 1
        else:
            decision = self.players[self.current_player].make_decision()
            if decision:
                decision()

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
