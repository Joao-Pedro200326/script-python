import pygame

pygame.init()

def anime():
    l = [pygame.image.load(f'Dead ({x}).png') for x in range(1, 13)]
    while True:
        for frame in l:
            yield frame

janela = pygame.display.set_mode((600, 600))
relogio = pygame.time.Clock()
a = anime()
while True:
    relogio.tick(15)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    janela.fill((0, 0, 0))
    janela.blit(a.__next__(), (0, 0))
    pygame.display.update()
