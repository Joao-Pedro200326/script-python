import pygame


def animacao():
    while True:
        for num, img in enumerate([pygame.image.load(f'data/zombies/male/attack/Attack ({x}).png') for x in range(1, 9)]):
            if num == 3:
                yield [img]
            else:
                yield img
