

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
        self.handlers.append((handler, filters))

    def trigger(self, attacker, defender, unit_amount):
        if not defender.conquerable() or attacker.unit_amount <= 1:
            return False

        unit_amount = min(unit_amount, attacker.unit_amount-1)
        winner = ''
        if defender.unit_amount:
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
        attacker.unit_amount -= unit_amount

        for handler, filters in self.handlers:
            is_attacker = filters['attacker'] in (attacker, None)
            is_defender = filters['defender'] in (defender, None)
            same_winner = filters['winner'] in (winner, None)
            if is_attacker and is_defender and same_winner:
                handler(attacker, defender, unit_amount, winner)
        return True
