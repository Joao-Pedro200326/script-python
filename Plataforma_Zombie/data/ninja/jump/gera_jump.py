import pygame


def animacao():
    for img in [pygame.image.load(f'data/ninja/jump/Jump__{x}.png') for x in range(10)]:
        yield img
    while True:
        yield pygame.image.load('data/ninja/jump/Jump__9.png')
