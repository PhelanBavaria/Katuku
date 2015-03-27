

from common.events import Event


class ChangeOwner(Event):
    def __init__(self, campaign):
        Event.__init__(self)
        self.campaign = campaign

    def on_trigger(self, handler, province=None, country=None):
        filters = {
            'province': province,
            'country': country
        }
        self.handlers.add((handler, filters))

    def trigger(self, province, country):
        if province.controller == country:
            return False

        province.controller = country

        for handler, filters in self.handlers:
            is_province = filters['province'] in (province, None)
            is_country = filters['country'] in (country, None)
            if is_province and is_country:
                handler()

        return True
