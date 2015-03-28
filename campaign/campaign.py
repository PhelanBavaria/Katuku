

import os
import random
from pygame import image
from campaign import Country
from campaign import Province
from campaign import controllers
from campaign.events import ChangeOwner
from campaign.events import ReceiveUnits
from campaign.events import AmassUnits
from campaign.events import Attack
from campaign.events import SelectProvince


class Campaign:
    def __init__(self, setup):
        self.setup = setup
        self.paused = False
        self.current_player = 0
        self.map_name = ''
        self.events = {
            'change_owner': ChangeOwner(self),
            'receive_units': ReceiveUnits(self),
            'amass_units': AmassUnits(self),
            'attack': Attack(self),
            'select_province': SelectProvince(self)
        }
        self.players = [controllers.types[p](n, self, Country(c)) for p, n, c
                        in setup['players']]
        self.gamerules = setup['rules']
        self.provinces = {}

    def create(self):
        self.load_map(self.setup['map'])
        provinces = list(self.provinces.values())

        if self.gamerules['auto_unit_placement']:
            if self.gamerules['start_province_limit']:
                for i in range(self.gamerules['start_province_limit']):
                    for player in self.players:
                        if not provinces:
                            break
                        province = random.choice(provinces)
                        while not province.occupiable():
                            provinces.remove(province)
                            province = random.choice(provinces)
                        self.events['change_owner'].trigger(province, player.country)
                        self.events['amass_units'].trigger(province)
                        provinces.remove(province)
                    if not provinces:
                        break
            else:
                while provinces:
                    for player in self.players:
                        if not provinces:
                            break
                        province = random.choice(provinces)
                        while not province.occupiable():
                            provinces.remove(province)
                            province = random.choice(provinces)
                        self.events['change_owner'].trigger(province, player.country)
                        self.events['amass_units'].trigger(province)
                        provinces.remove(province)

            for player in self.players:
                units = self.gamerules['start_units'] * \
                        len(player.country.provinces)
                player.country.units_to_place += units
                self.random_placement(player.country)
        else:
            print('Not implemented yet that province are selected manually')

        if self.gamerules['fill_remaining_provinces']:
            independent = controllers.Independent(self)
            for province in provinces:
                if not province.conquerable():
                    continue
                self.events['change_owner'].trigger(province, independent.country)
                self.events['amass_units'].trigger(province)
            provinces = []
            units = self.gamerules['start_units'] * \
                    len(independent.country.provinces)
            independent.country.units_to_place += units
            self.random_placement(independent.country)
            self.players.append(independent)


    def update(self):
        current_player = self.players[self.current_player]
        if not current_player.placement_done:
            current_player.place_unit()
        elif not current_player.attacking_done:
            current_player.attack()
        else:
            print('Player', current_player.name, 'ready')
            country = current_player.country
            self.events['receive_units'].trigger(country)
            if self.gamerules['auto_unit_placement']:
                self.random_placement(country)
            self.current_player += 1
        if self.current_player == len(self.players):
            self.current_player = 0
            for player in self.players:
                player.placement_done = False
                player.attacking_done = False
            print('End Turn')

    def random_placement(self, country):
        provinces = country.provinces[:]
        while provinces and country.units_to_place:
            color = random.choice(provinces)
            province = self.provinces[color]
            if not self.events['amass_units'].trigger(province):
                provinces.remove(color)

    def load_map(self, name):
        file_name = name + '.bmp'
        print('Loading map:', file_name)
        self.map_name = name
        surface = image.load(os.path.join('campaign', 'maps', file_name))
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
