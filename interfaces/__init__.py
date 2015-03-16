from interfaces.base import Base
from interfaces.player import Player
from interfaces.local_player import LocalPlayer
from interfaces.ai import AI
from interfaces.tracer import Tracer
from interfaces.command_line import CommandLine
from interfaces.gui import GUI

player_types = {
    'local': LocalPlayer,
    'ai': AI
}
