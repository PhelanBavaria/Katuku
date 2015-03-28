

from common.events import Event


class AmassUnits(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, province_id=None):
        filters = {
            'province_id': province_id
        }
        self.handlers.append((handler, filters))

    def trigger(self, province, unit_amount=1):
        max_units = self.campaign.gamerules['max_units_province']
        unit_cap = province.unit_amount >= max_units
        if unit_cap or province.controller.units_to_place <= 0:
            return False

        unit_amount = min(unit_amount, max_units - province.unit_amount)
        province.controller.units_to_place -= unit_amount
        province.unit_amount += unit_amount

        for handler, filters in self.handlers:
            is_id = filters['province_id'] in (province.color, None)
            if is_id:
                handler(province)

        return True
