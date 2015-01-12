

from interfaces import Base
from interfaces import Player
from interfaces import AI


class CommandLine(Base):
    counter = 0
    last_action = None

    def __init__(self, game):
        Base.__init__(self, game)
        self.actions = {
            'exit': self.exit,
            'exec': self._exec
        }

    def update(self):
        if self.counter:
            self.last_action()
            self.counter -= 1
        else:
            command = input('>>> ')
            try:
                action = self.actions[command]
            except KeyError:
                print('Action not supported')
                return
            action()

    def _exec(self):
        if self.game.config['exec']:
            exec(input('\t'))
        else:
            print('You are not allowed to use this command')
        return True

    def exit(self):
        self.game.run = False

    def select_province(self, hex_color):
        self.game.selected_prov = hex_color

