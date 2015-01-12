

import random
from common import util
from interfaces import Player


class AI(Player):
    def update(self):
        if self.units_to_place:
            while True:
                provinces = list(self.game.campaign.provinces.values())
                province = random.choice(provinces)
                if not province.controller:
                    self.units_to_place -= 1
                    province.battle(self, 1)
                    self.game.campaign.end_turn()
                    break

