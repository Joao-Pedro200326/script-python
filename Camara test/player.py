import pygame
from pygame import *
from variaveis import *


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.iventario = []
        self.image = pygame.Surface((50, 50))
        self.image.fill((50,100,200))
        self.rect = self.image.get_rect()
        self.rect.center = (400, 300)
    
    def update(self):
        keys = pygame.key.get_pressed()
        vel_x = 0
        vel_y = 0
        if keys[K_d]:
            vel_x += P_VEL
        elif keys[K_a]:
            vel_x -= P_VEL
        if keys[K_w]:
            vel_y -= P_VEL
        elif keys[K_s]:
            vel_y += P_VEL
        
        if vel_y != 0 and vel_x != 0:
            vel_x = -P_VELM if vel_x < 0 else P_VELM
            vel_y = -P_VELM if vel_y < 0 else P_VELM

        self.rect.x += vel_x
        self.rect.y += vel_y

        #print(f'x: {self.rect.centerx} y: {self.rect.centery}')


class Camara():
    def __init__(self, tamanho):
        self.tamanho = tamanho
        self.imagem = None
    
    def draw(self, alvo, surf_mapa):
        try:
            return surf_mapa.subsurface(alvo.rect.centerx - self.tamanho[0]//2, alvo.rect.centery -self.tamanho[1]//2, self.tamanho[0], self.tamanho[1])
        except ValueError:
            x = alvo.rect.centerx - self.tamanho[0]//2
            if x > surf_mapa.get_width() - self.tamanho[0]:
                x = surf_mapa.get_width() - self.tamanho[0]
            elif x < 0:
                x = 0
            y = alvo.rect.centery - self.tamanho[1]//2
            if y > surf_mapa.get_height() - self.tamanho[1]:
                y = surf_mapa.get_height() - self.tamanho[1]
            elif y < 0:
                y = 0
            return surf_mapa.subsurface(x, y, self.tamanho[0], self.tamanho[1])
