

import pygame


class Overlay(pygame.Surface):
    def __init__(self, surface):
        self.surface = surface.copy()

    def update(self, province):
        pass

