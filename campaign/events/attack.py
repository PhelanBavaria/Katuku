

import random
from common.events import Event


class Attack(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, attacker=None, defender=None,
                   winner=None):
        filters = {
            'attacker': attacker,
            'defender': defender,
            'winner': winner
        }
        self.handlers.add((handler, filters))

    def trigger(self, attacker, defender, unit_amount):
        if self.defender.conquerable():
            return False

        unit_amount = min(unit_amount, attacker.unit_amount-1)
        winner = ''

        if not defender.unit_amount:
            gamerules = self.campaign.gamerules
            da = min((unit_amount, gamerules['max_dice_attack']))
            dd = min((defender.unit_amount, gamerules['max_dice_defence']))
            sa = sum([random.randint(1, 6) for i in range(da)])
            sd = sum([random.randint(1, 6) for i in range(dd)])
            if sa <= sd:
                winner = 'defender'
            else:
                winner = 'attacker'
                defender.unit_amount = unit_amount
                defender.controller = attacker.controller
        else:
            winner = 'attacker'
            defender.unit_amount = unit_amount
            defender.controller = attacker.controller

        for handler, filters in self.handlers:
            is_attacker = filters['attacker'] in (attacker.name, None)
            is_defender = filters['defender'] in (defender.name, None)
            same_winner = filters['winner'] in (winner, None)
            if is_attacker and is_defender and same_winner:
                handler()

        return True
