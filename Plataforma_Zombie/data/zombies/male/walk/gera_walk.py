import pygame


def animacao():
    while True:
        for img in [pygame.image.load(f'data/zombies/male/walk/Walk ({x}).png') for x in range(1, 11)]:
            yield img
