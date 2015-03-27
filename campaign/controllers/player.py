



class Player:
    def __init__(self, name, campaign, country=None):
        self.name = name
        self.campaign = campaign
        self.country = country
        self.ready = False
        campaign.events['select_province'].on_trigger(self.on_province_selection)

    def make_decision(self):
        if not self.country:
            return

        if not self.country.origin_province:
            self.country.goal_province = None
        elif self.country.units_to_place > 0:
            return self.place_unit()
        elif self.country.goal_province:
            return self.attack()

    def attack(self):
        pass

    def place_unit(self):
        pass

    def on_province_selection(self, action):
        pass

    def bordering_provinces(self):
        for province in self.provinces:
            for neighbour in province.neighbours:
                if neighbour not in self.provinces:
                    yield neighbour
