import pygame


def animacao():
    for img in [pygame.image.load(f'data/zombies/male/dead/Dead ({x}).png') for x in range(1, 12)]:
        yield img
    yield pygame.image.load('data/zombies/male/dead/Dead (12).png')
