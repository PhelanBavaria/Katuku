

import random
from common.actions import Action


class Attack(Action):
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
                Action.__call__(self)
                return
        self.won = True
        self.defender.unit_amount = self.unit_amount
        self.defender.controller = self.attacker.controller
        Action.__call__(self)
