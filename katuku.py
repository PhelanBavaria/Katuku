

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
gui = GUI(game)
gui.pages['page_campaign'] = PageCampaign(gui)
game.local_interface = gui

# Test:
players = [
    Player('test_human', (0, 0, 255), game),
    AI('test_ai', (255, 0, 0), game)
]
setup = {
    'map': 'test',
    'start_units': 4,
    'remaining_provinces_filled_by': 'independent',
    'players': players
}
game.campaign = Campaign(setup)
#game.campaign.select_provinc'#00ff00')


while game.run:
    game.update()
    if game.campaign and not game.campaign.paused:
        game.campaign.update()
