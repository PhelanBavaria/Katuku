

import yaml


class Country:
    def __init__(self, name):
        self.name = name
        self.units_to_place = 0
        self.provinces = []
        self.origin_province = None
        self.goal_province = None
        try:
            country = yaml.load(open('content/countries/' + name + '.yml').read())
            self.prim_color = country['prim_color']
            self.sec_color = country['sec_color']
        except OSError:
            self.prim_color = (255, 0, 0, 255)
            self.sec_color = (0, 0, 0, 255)

    def save(self):
        country = {'prim_color': self.prim_color, 'sec_color': self.sec_color}
        dump = yaml.dump(country, default_flow_style=False)
        open('content/countries/' + self.name + '.yml', 'w+').write(dump)
