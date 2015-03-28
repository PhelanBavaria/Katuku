



class Player:
    def __init__(self, name, campaign, country=None):
        self.name = name
        self.campaign = campaign
        self.country = country
        self.placement_done = False
        self.attacking_done = False
        campaign.events['select_province'].on_trigger(self.on_province_selection)

    def attack(self):
        pass

    def place_unit(self):
        pass

    def on_province_selection(self, color):
        pass

    def bordering_provinces(self):
        for province in self.provinces:
            for neighbour in province.neighbours:
                if neighbour not in self.provinces:
                    yield neighbour

    def unfull_provinces(self):
        for color in self.country.provinces:
            province = self.campaign.provinces[color]
            if province.unit_amount >= self.campaign.gamerules['max_units_province']:
                yield province
