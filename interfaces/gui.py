

import os
import pygame
from interfaces import Base
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
            pygame.K_ESCAPE: self.exit,
            pygame.K_RETURN: None
        }
        pygame.display.flip()

    def update(self):
        for event in pygame.event.get():
            try:
                self.interactions[event.type]()
            except KeyError:
                try:
                    self.interactions[event.key]()
                except KeyError:
                    continue
                except AttributeError:
                    continue
            except AttributeError:
                continue

        for widget in self.widgets.values():
            widget.draw(self.screen)
        pygame.display.flip()

    def exit(self):
        self.game.run = False

    def select_widget(self):
        pos = pygame.mouse.get_pos()
        for widget in self.widgets:
            if widget.get_rect().collidepoint(*pos):
                widget.on_click()
                self.selected_widget = widget
                break

    def draw_game(self):
        self.screen.blit(self.game.prov_map, (0, 0))
        if self.game.selected_prov:
            color = (255, 255, 255)
            province = self.game.provinces[self.game.selected_prov]
            for x, y in province.border:
                self.screen.fill(color, pygame.Rect(x, y, 1, 1))
