

import os
import pygame
import pygame.freetype
from interfaces import Base
from interfaces import LocalPlayer
from common.widgets import GameMap


class GUI(Base):
    def __init__(self, game):
        Base.__init__(self, game)
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Katuku')
        map_path = os.path.join('content', 'maps', game.campaign.map_name + '.bmp')
        self.widgets = {
            'campaignmap': GameMap(map_path, game)
        }
        self.displayed = []
        self.selected_widget = None
        self.interactions = {
            pygame.QUIT: self.exit,
            pygame.MOUSEBUTTONDOWN: self.select_widget,
            pygame.MOUSEMOTION: self.hover_widget,
            pygame.K_ESCAPE: self.exit,
            pygame.K_RETURN: self.end_turn
        }
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            try:
                interaction = self.interactions[event.type]
            except KeyError:
                try:
                    interaction = self.interactions[event.key]
                except KeyError:
                    continue
                except AttributeError:
                    continue
            except AttributeError:
                continue
            interaction()

        for widget in self.widgets.values():
            widget.draw(self.screen)
        pygame.display.flip()

    def exit(self):
        self.game.run = False

    def end_turn(self):
        player = self.game.campaign.players[self.game.campaign.current_player]
        if type(player) == LocalPlayer:
            player.ready = True

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

    def draw_game(self):
        self.screen.blit(self.game.prov_map, (0, 0))
        if self.game.selected_prov:
            color = (255, 255, 255)
            province = self.game.provinces[self.game.selected_prov]
            for x, y in province.border:
                self.screen.fill(color, pygame.Rect(x, y, 1, 1))
