

import yaml
import pygame
from common import Game
from interfaces import GUI
from interfaces import CommandLine
from common import Campaign
from content.pages import Campaign as PageCampaign
from interfaces import Player
from interfaces import AI



pygame.init()

game = Game()
game.local_interface = CommandLine(game)
# gui = GUI(game)
# gui.pages['page_campaign'] = PageCampaign(gui)
# game.local_interface = gui

# Test:
players = [
    Player('test_human', game),
    AI('test_ai', game)
]
rules = yaml.load(open('content/gamerules/dicewars.yml').read())
setup = {
    'map': 'Europe',
    'rules': rules
    'players': players
}
game.campaign = Campaign(setup)
#game.campaign.select_provinc'#00ff00')


while game.run:
    game.update()
    if game.campaign and not game.campaign.paused:
        game.campaign.update()
