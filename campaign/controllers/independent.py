

from campaign.controllers import AI
from campaign import Country


class Independent(AI):
    def __init__(self, campaign):
        AI.__init__(self, 'Independent', campaign, Country('Independent'))
        self.country.prim_color = (200, 200, 200, 255)
        self.country.sec_color = (150, 150, 150, 255)

    def attack(self):
        self.attacking_done = True
        return
