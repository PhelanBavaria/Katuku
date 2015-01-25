

import yaml


class Game:
    run = True
    local_interface = None
    campaign = None
    config = yaml.load(open('config.yml').read())
    keymap = yaml.load(open('keymap.yml').read())
    keys_down = set()
    controllers = []

    def update(self):
        self.local_interface.update()
        self.keys_down = set()
