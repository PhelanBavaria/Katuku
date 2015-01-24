

import os
import random
from time import time
from pygame import image
from common import util
from common import Province
from common import Trigger


class Campaign:
    def __init__(self, setup):
        self.setup = setup
        self.paused = False
        self.history = {}
        self.current_player = 0
        self.turn = []
        self.unready_players = []
        self.map_name = ''
        self.players = setup['players']
        self.gamerules = setup['rules']
        self.provinces = {}
        self.triggers = {
            'select_province': Trigger()
        }
        self.set_up()
        print('Turn:', self.players[self.current_player].name)

    def set_up(self):
        self.load_map(self.setup['map'])
        if self.gamerules['auto_unit_placement']:
            unassigned = list(self.provinces.keys())
            pt = len(self.provinces)
            su = self.gamerules['start_units']
            for player in self.players:
                for i in range(int(pt*su)):
                    if unassigned:
                        choice = random.choice(unassigned)
                        unassigned.remove(choice)
                        player.provinces.append(choice)
                        self.provinces[choice].controller = player.name
                    else:
                        choice = random.choice(player.provinces)
                    self.provinces[choice].unit_amount += 1
        self.unready_players = self.players

    def update(self):
        for player in self.unready_players[:]:
            if not player.ready:
                action = player.update()
                self.turn.append(action)
                if not self.gamerules['simultanious_turns']:
                    break
            else:
                if not self.gamerules['simultanious_turns']:
                    self.end_turn()
                self.unready_players.remove(player)
        if not self.unready_players:
            if self.gamerules['simultanious_turns']:
                self.end_turn()
            [player.ready = False for player in self.players]
            self.unready_players = self.players

    def end_turn(self):
        for action in self.turn:
            self.actions[action[0]](action[1:])
        print('Turn:', self.players[self.current_player].name)

    def add_history(self, action, info):
        if self.turn not in self.history.keys():
            self.history[self.turn] = {}
        if action not in self.history[self.turn].keys():
            self.history[self.turn][action] = []
        self.history[self.turn][action].append(info)

    def load_map(self, name):
        print('Loading map:', name + '.bmp')
        self.map_name = name
        surface = image.load(os.path.join('content', 'maps', name + '.bmp'))
        width, height = surface.get_width(), surface.get_height()
        for y in range(height):
            last_color = None
            for x in range(width):
                color = tuple(surface.get_at((x, y)))
                if color not in self.provinces.keys():
                    self.provinces[color] = Province(self)
                    if all([c <= 90 for c in value]):
                        self.provinces[color].passable = False
                    elif value[2] == 255:
                        self.provinces[color].water = True
                if not last_color:
                    last_color = color
                    continue
                if last_color != color:
                    self.provinces[color].neighbours.add(last_color)
                    self.provinces[last_color].neighbours.add(color)
                    last_color = color
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
