

from common.events import Event


class ReceiveUnits(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, country=None):
        filters = {
            'country': country
        }
        self.handlers.add((handler, filters))

    def trigger(self, country):
        province_units = self.campaign.gamerules['new_units_per_turn']
        if callable(province_units):
            province_units = province_units(self.campaign, country)
        else:
            province_units = province_units
        country.units_to_place += province_units

        for handler, filters in self.handlers:
            is_country = filters['country'] in (country, None)
            if is_country:
                handler()

        return True
