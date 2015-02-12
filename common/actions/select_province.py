

from common.actions import Action


class SelectProvince(Action):
    subscribers = []
    def __init__(self, campaign, color):
        self.campaign = campaign
        self.color = color
