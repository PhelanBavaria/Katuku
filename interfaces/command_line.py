

from interfaces import Base
from interfaces import Tracer
from common import actions


class CommandLine(Base):
    counter = 0

    def __init__(self, game):
        Base.__init__(self, game)
        self.actions = {
            '': self._pass,
            'exit': self.exit,
            'exec': self._exec,
            'skip': self.skip,
            'select_province': self.select_province
        }
        tracer = Tracer(game)

    def update(self):
        while True:
            if self.counter:
                self.counter -= 1
                break
            else:
                command = input('>>> ')
                try:
                    action = self.actions[command]
                except KeyError:
                    print('Action not supported')
                    break
                if action():
                    break

    def _pass(self):
        return True

    def _exec(self):
        if self.game.config['exec']:
            exec(input('\t'))
        else:
            print('You are not allowed to use this command')

    def exit(self):
        self.game.run = False
        return True

    def skip(self):
        self.counter = int(input('\t'))-1
        return True

    def select_province(self):
        rgb_color = input('\tRGB: ')
        rgb_color = rgb_color.split(' ')
        if len(rgb_color) == 3:
            rgb_color.append(255)
        elif len(rgb_color) != 4:
            print('Not a valid RGB color!')
            return
        actions.SelectProvince(self.game.campaign, rgb_color)()
