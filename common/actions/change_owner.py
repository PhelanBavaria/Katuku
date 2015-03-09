

from common.actions import Action


class ChangeOwner(Action):
    subscribers = []
    def __init__(self, province, player):
        self.province = province
        self.player = player

    def __call__(self):
        if not self.useable():
            return False
        Action.__call__(self)
        self.province.controller = self.player
        return True

    def useable(self):
        same_controller = self.province.controller == self.player
        return not same_controller
