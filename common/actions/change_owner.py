

from common.actions import Action


class ChangeOwner(Action):
    subscribers = []
    def __init__(self, province, country):
        self.province = province
        self.country = country

    def __call__(self):
        if not self.useable():
            return False
        Action.__call__(self)
        self.province.controller = self.country
        return True

    def useable(self):
        same_controller = self.province.controller == self.country
        return not same_controller
