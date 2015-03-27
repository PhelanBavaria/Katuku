

from common.events import Event


class SelectProvince(Event):
    subscribers = []
    def __init__(self, campaign, color):
        self.campaign = campaign
        self.color = color
