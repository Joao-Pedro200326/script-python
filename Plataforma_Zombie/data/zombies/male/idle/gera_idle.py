import pygame


def animacao():
    while True:
        for img in [pygame.image.load(f'data/zombies/male/idle/Idle ({x}).png') for x in range(1, 16)]:
            yield img
