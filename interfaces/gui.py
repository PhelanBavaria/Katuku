

import pygame
import pygame.freetype
from interfaces import Base
from campaign.controllers import LocalPlayer
from common.widgets import CampaignMap


class GUI(Base):
    def __init__(self, game):
        Base.__init__(self, game)
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Katuku')
        self.widgets = {}
        self.selected_widget = None
        self.interactions = {
            pygame.QUIT: self.exit,
            pygame.MOUSEBUTTONDOWN: self.select_widget,
            pygame.MOUSEMOTION: self.hover_widget,
            pygame.KEYDOWN: self.key_down,
            pygame.KEYUP: self.key_up
        }
        self.on_key_down = {}
        self.on_key_up = {}
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            try:
                self.interactions[event.type](event)
            except TypeError:
                self.interactions[event.type]()
            except KeyError:
                continue

        for widget in self.widgets.values():
            widget.draw(self.screen)
        pygame.display.flip()

    def key_down(self, event):
        try:
            self.on_key_down[event.key]()
        except KeyError:
            return

    def key_up(self, event):
        try:
            self.on_key_up[event.key]()
        except KeyError:
            return

    def exit(self):
        self.game.run = False

    def end_turn(self):
        player = self.game.campaign.players[self.game.campaign.current_player]
        if type(player) == LocalPlayer:
            if not player.placement_done:
                player.placement_done = True
            elif not player.attacking_done:
                player.attacking_done = True

    def select_widget(self):
        x, y = pygame.mouse.get_pos()
        for widget in self.widgets.values():
            if widget.get_rect().collidepoint(x, y):
                widget.on_click()
                self.selected_widget = widget
                break

    def hover_widget(self):
        x, y = pygame.mouse.get_pos()
        for widget in self.widgets.values():
            if widget.get_rect().collidepoint(x, y):
                widget.on_hover()
                break

    def show_campaign(self):
        self.widgets.clear()
        self.widgets['campaignmap'] = CampaignMap(self.game.campaign)
        self.on_key_down = {
            pygame.K_ESCAPE: self.exit,
            pygame.K_RETURN: self.end_turn
        }
