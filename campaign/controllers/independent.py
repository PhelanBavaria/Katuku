

from campaign.controllers import AI


class Independent(AI):
    def attack(self):
        self.ready = True
        return
