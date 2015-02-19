

from interfaces import Base
from common import actions


class Tracer(Base):
    def __init__(self, game):
        actions.SelectProvince.subscribers.append(self.on_select_province)
        actions.PlaceUnit.subscribers.append(self.on_place_unit)
        actions.Attack.subscribers.append(self.on_attack)
        actions.ReceiveUnits.subscribers.append(self.on_receive_units)

    def on_select_province(self, action):
        print('Province', action.color, 'selected')

    def on_receive_units(self, action):
        print('Player', action.player.name, 'received', action.province_units,
              'units from provinces and', action.extra_units, 'extra units')

    def on_place_unit(self, action):
        print('Player', action.player.name, 'placed', action.unit_amount,
              'units on', action.province.color)

    def on_attack(self, action):
        attacker = action.attacker.controller.name
        try:
            defender = action.defender.controller.name
        except AttributeError:
            defender = None
        if action.won:
            result = 'won'
        else:
            result = 'lost'
        print('Player', attacker,
              'attacked', action.defender_unit_amount, 'units on',
              action.defender.color, '(' + str(defender) + ')',
              'from', action.attacker.color,
              'with', action.unit_amount, 'out of',
              action.attacker.unit_amount+action.unit_amount, 'units',
              'and', result,
              '(', action.defender_dice, 'vs.', action.attacker_dice, ')')
