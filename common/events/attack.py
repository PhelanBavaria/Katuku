

import random
from common.events import Event


class Attack(Event):
    subscribers = []
    def __init__(self, campaign, defender, attacker, unit_amount):
        self.campaign = campaign
        self.defender = defender
        self.attacker = attacker
        self.unit_amount = unit_amount
        self.defender_unit_amount = defender.unit_amount
        self.attacker_dice = 0
        self.defender_dice = 0
        self.won = False

    def __call__(self):
        if not self.useable():
            return False

        left = self.attacker.unit_amount - self.unit_amount
        if left <= 0:
            self.unit_amount += left-1
            self.attacker.unit_amount = 1
        else:
            self.attacker.unit_amount -= self.unit_amount
        if self.defender.unit_amount:
            ps = self.campaign.provinces
            gamerules = self.campaign.gamerules
            da = min((self.unit_amount, gamerules['max_dice_attack']))
            dd = min((self.defender.unit_amount, gamerules['max_dice_defence']))
            sa = sum([random.randint(1, 6) for i in range(da)])
            sd = sum([random.randint(1, 6) for i in range(dd)])
            self.attacker_dice = sa
            self.defender_dice = sd
            if sa <= sd:
                #Event.__call__(self)
                return True
        self.won = True
        self.defender.unit_amount = self.unit_amount
        self.defender.controller = self.attacker.controller
        Event.__call__(self)
        return True

    def useable(self):
        return self.defender.conquerable()
