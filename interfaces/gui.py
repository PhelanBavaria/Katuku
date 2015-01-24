

import pygame
from interfaces import Base
from interfaces import CommandLine
from common.widgets import GameMap


class GUI(Base):
    def __init__(self, game):
        Base.__init__(self, game)
        self.console = CommandLine(game)
        self.screen = pygame.display.set_mode((800, 800))
        pygame.display.set_caption('Katuku')
        pygame.display.flip()

        self.pages = {}
        self.current_page = ''
        self.interactions = {
            pygame.QUIT: self.exit,
            pygame.MOUSEBUTTONDOWN: self.select_widget,
            pygame.K_ESCAPE: self.exit,
            pygame.K_RETURN: self.end_turn
        }

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

        if self.game.campaign:
            self.current_page = 'page_campaign'
        if self.current_page in self.pages.keys():
            self.pages[self.current_page].draw()
        else:
            print('Page "' + self.current_page + '" not existent!')
        pygame.display.flip()
        self.console.update()

    def exit(self):
        self.game.run = False

    def end_turn(self):
        self.game.campaign.end_turn()

    def select_widget(self):
        page = self.pages[self.current_page]
        pos = pygame.mouse.get_pos()
        for widget in page.widgets:
            if widget.get_rect().collidepoint(*pos):
                widget.on_click()
                page.selected_widget = widget
                break

    def draw_game(self):
        self.screen.blit(self.game.prov_map, (0, 0))
        if self.game.selected_prov:
            color = (255, 255, 255)
            province = self.game.provinces[self.game.selected_prov]
            for x, y in province.border:
                self.screen.fill(color, pygame.Rect(x, y, 1, 1))
