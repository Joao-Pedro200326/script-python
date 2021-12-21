import pygame


def animacao():
    while True:
        for img in [pygame.image.load(f'data/ninja/run/Run__{x}.png') for x in range(10)]:
            yield img
