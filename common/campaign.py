

import os
from time import time
from pygame import image
from common import util
from common import Province


class Campaign:
    def __init__(self, setup):
        self.setup = setup
        self.paused = False
        self.history = {}
        self.current_player = 0
        self.turn = 0
        self.map_name = ''
        self.players = setup['players']
        self.prov_map = None
        self.provinces = {}
        self.selected_province = ''
        self.origin_province = ''
        self.goal_province = ''
        self.load_map(setup['map'])
        for player in self.players:
            player.units_to_place = setup['start_units']
        print('Turn:', self.players[self.current_player].name)

    def update(self):
        player = self.players[self.current_player]
        player.update()

    def end_turn(self):
        self.selected_province = ''
        self.origin_province = ''
        self.goal_province = ''
        self.current_player += 1
        self.current_player %= len(self.players)
        if not self.current_player:
            self.turn += 1
        print('Turn:', self.players[self.current_player].name)

    def add_history(self, action, info):
        if self.turn not in self.history.keys():
            self.history[self.turn] = {}
        if action not in self.history[self.turn].keys():
            self.history[self.turn][action] = []
        self.history[self.turn][action].append(info)

    def load_map(self, name):
        print('Loading map:', name + '.bmp')
        start_time = time()
        self.map_name = name
        surface = image.load(os.path.join('content', 'maps', name + '.bmp'))
        width, height = surface.get_width(), surface.get_height()
        px_count = width*height
        progress = 0
        for y in range(height):
            for x in range(width):
                new_progress = int((width*y+x+1)/px_count*100)
                if new_progress != progress and not new_progress % 10:
                    progress = new_progress
                    print('Progress:', str(progress) + '%')
                color = surface.get_at((x, y))
                color = '#%02x%02x%02x' % color[0:3]
                if color not in self.provinces.keys():
                    self.provinces[color] = Province(self, color)
                self.provinces[color].pixels.append((x, y))
                for adjacent in util.adjacent((x, y)):
                    try:
                        adj_color = surface.get_at(adjacent)
                    except IndexError:
                        self.provinces[color].border.append((x, y))
                        continue
                    adj_color = '#%02x%02x%02x' % adj_color[0:3]
                    if adj_color != color:
                        self.provinces[color].border.append((x, y))
                        self.provinces[color].neighbours.add(adj_color)
        self.prov_map = surface
        print('Completion time:', time() - start_time)
