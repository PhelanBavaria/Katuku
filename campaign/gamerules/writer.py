

import yaml
import new_units_per_turn

name = 'dicewars'
rules = {
'start_units': 5,        # %, provinces / players * 5
'fill_remaining_provinces': True,
'auto_unit_placement': True,
'simultanious_turns': False,
'new_units_per_turn': new_units_per_turn.max_connected_provinces,
'auto_turn': False,        # True, False
'max_dice_attack': 8,
'max_dice_defence': 8,
'max_units_province': 8,
'choice_unit_tally_on_attack': False
}

dump = yaml.dump(rules, default_flow_style=False)
open(name + '.yml', 'w+').write(dump)
