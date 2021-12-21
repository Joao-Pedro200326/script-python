import pygame
from settings import *


class Camara:
    def __init__(self, width, height):
        self.camara = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity):
        return entity.rect.move(self.camara.topleft)

    def update(self, target, mapa_size):
        x = -target.rect.centerx + largura // 2
        y = -target.rect.centery + altura // 2

        x = min(0, x)
        y = min(0, y)
        x = max(-(mapa_size[0] - largura), x)
        y = max(-(mapa_size[1] - altura), y)
        self.camara = pygame.Rect(x, y, self.width, self.height)


class Mapa:
    def __init__(self):
        self.mapa = []
        with open('data/map_01.txt', 'r') as arq:
            for linha in arq.readlines():
                self.mapa.append(linha.replace('\n', ''))
        self.size = (len(self.mapa[-1])*tilesize, len(self.mapa)*tilesize)

