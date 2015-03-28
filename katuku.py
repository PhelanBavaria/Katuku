

import random
import logging
import yaml
import pygame
from common import Game
from campaign import Campaign
from interfaces import GUI



random.seed(222)
pygame.init()
logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)

game = Game()

# Test:
players = [
    ('local', 'test_p1', '__BAVARIA__'),
    ('ai', 'test_p2', '__TESTIA__')
]
rules = yaml.load(open('campaign/gamerules/capital_expansion.yml').read())
setup = {
    'map': 'Europe',
    'rules': rules,
    'players': players
}
game.campaign = Campaign(setup)
game.campaign.create()
#game.campaign.select_provinc'#00ff00')
# game.local_interface = Tracer(game)
# game.local_interface = CommandLine(game)
game.local_interface = GUI(game)
game.local_interface.show_campaign()
# gui.pages['page_campaign'] = PageCampaign(gui)
# game.local_interface = gui


while game.run:
    game.update()
    remaining = [player for player in game.campaign.players
                 if len(player.country.provinces)]
    if len(remaining) == 1:
        logging.info('Player ' + remaining[0].name + ' has won!')
        logging.info('Occupied provinces: ' + str(len(remaining[0].provinces)))
        if input('Type anything to end'):
            break
    elif game.campaign and not game.campaign.paused:
        game.campaign.update()
    #for player in players:
        #print('Player', player.name, 'owns', len(player.provinces), 'provinces')
        #print(player.provinces)
