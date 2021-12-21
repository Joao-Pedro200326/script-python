import pygame


def animacao():
    for num, img in enumerate([pygame.image.load(f'data/ninja/throw/throw__{x}.png') for x in range(10)]):
        if num == 3:
            yield [img]
        else:
            yield img
