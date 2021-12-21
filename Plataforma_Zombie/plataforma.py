import pygame
from settings import *


def hex_num(char):
    dic = {'a': 10, 'b': 11, 'c': 12, 'd': 13, 'e': 14, 'f': 15}
    for c in dic.keys():
        if c == char:
            return dic[c]
    return char


class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, c):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load(f'data/cenario/Tiles/Tile ({hex_num(c)}).png'),
                                            (tilesize, tilesize))
        self.rect = self.image.get_rect()
        self.rect.x = x * tilesize
        self.rect.y = y * tilesize
