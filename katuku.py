

import random
import yaml
import pygame
from common import Game
from interfaces import GUI
from interfaces import CommandLine
from interfaces import Tracer
from common import Campaign
from content.pages import Campaign as PageCampaign
from interfaces import Player
from interfaces import AI



random.seed(222)
pygame.init()

game = Game()
game.local_interface = Tracer(game)
# game.local_interface = CommandLine(game)
# gui = GUI(game)
# gui.pages['page_campaign'] = PageCampaign(gui)
# game.local_interface = gui

# Test:
players = [
    AI('test_p1', game),
    AI('test_p2', game)
]
rules = yaml.load(open('content/gamerules/dicewars.yml').read())
setup = {
    'map': 'Europe',
    'rules': rules,
    'players': players
}
game.campaign = Campaign(setup)
game.campaign.create()
#game.campaign.select_provinc'#00ff00')


while game.run:
    game.update()
    remaining = [player for player in players if len(player.provinces)]
    if len(remaining) == 1:
        print('Player', remaining[0].name, 'has won!')
        print('Occupied provinces:', len(remaining[0].provinces))
        break
    elif game.campaign and not game.campaign.paused:
        game.campaign.update()
    #for player in players:
        #print('Player', player.name, 'owns', len(player.provinces), 'provinces')
        #print(player.provinces)
