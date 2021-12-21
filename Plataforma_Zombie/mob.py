import pygame
from settings import *
from random import randint
from data.zombies.male.idle import gera_idle
from data.zombies.male.walk import gera_walk
from data.zombies.male.attack import gera_attack
from data.zombies.male.dead import gera_dead

vetor2D = pygame.math.Vector2


class Mobmale(pygame.sprite.Sprite):
    def __init__(self, x, y, game):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.image = pygame.image.load('data/zombies/male/idle/Idle (1).png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.left = False
        self.walk = False
        self.attack = False
        self.dead = False
        self.idle_animacao = gera_idle.animacao()
        self.walk_animacao = gera_walk.animacao()
        self.attack_animacao = gera_attack.animacao()
        self.dead_animacao = gera_dead.animacao()
        self.vel = self.acl = vetor2D()
        self.vida = randint(50, 100)
        self.dano_de_ataque = randint(5, 15)

    def colisao_tiles(self):
        colisao = pygame.sprite.spritecollide(self, self.game.plataformas, False)
        for col_tile in colisao:
            if col_tile.rect.top < self.rect.bottom < col_tile.rect.bottom:
                self.rect.bottom = col_tile.rect.top + 1
                if self.vel.y - self.acl.y != -22:
                    self.vel.y = 0
            if col_tile.rect.bottom > self.rect.top > col_tile.rect.top:
                self.rect.top = col_tile.rect.bottom + 1
                self.vel.y = 0
            if col_tile.rect.left < self.rect.right < col_tile.rect.right \
                    and self.rect.top < col_tile.rect.y < self.rect.bottom - 2:
                self.rect.right = col_tile.rect.left
                self.vel.x = 0
            if col_tile.rect.right > self.rect.left > col_tile.rect.left \
                    and self.rect.top < col_tile.rect.y < self.rect.bottom - 2:
                self.rect.left = col_tile.rect.right
                self.vel.x = 0

    def dano(self, dano_normal):
        self.vida -= dano_normal + randint(-dano_normal//3, dano_normal//3)

    def causa_dano(self):
        self.game.player.vida -= (self.dano_de_ataque + randint(-10, 10))

    def update(self):
        if self.vida <= 0:
            if not self.dead:
                self.rect.y += 15
            self.dead = True

        self.acl = vetor2D(0, GRAVIDADE)
        self.walk = self.attack = False
        if self.game.player.vida > 0 and not self.dead:
            if self.rect.centerx - 500 < self.game.player.rect.centerx < self.rect.left:
                self.acl.x = -MOB_ACL
                self.left = self.walk = True
            elif self.rect.right < self.game.player.rect.centerx < self.rect.centerx + 500:
                self.acl.x = MOB_ACL
                self.left = False
                self.walk = True
            if self.rect.left - 10 < self.game.player.rect.centerx < self.rect.right + 10 \
                    and self.rect.top < self.game.player.rect.bottom and self.rect.bottom > self.game.player.rect.top:
                self.attack = True

            self.acl.x += self.vel.x * MOB_ATR
            self.vel += self.acl
            if 0 > self.vel.x > -0.4:
                self.vel.x = 0
                self.acl = vetor2D(0, GRAVIDADE)
            self.colisao_tiles()
            self.rect.center += self.vel + 0.5 * self.acl

        if self.dead:
            try:
                self.image = pygame.transform.flip(self.dead_animacao.__next__(), self.left, False)
            except StopIteration:
                self.rect.y += 1
                for plataforma in pygame.sprite.spritecollide(self, self.game.plataformas, False):
                    if plataforma.rect.top < self.rect.top + 50:
                        self.kill()
        elif self.attack:
            img = self.attack_animacao.__next__()
            if type(img) == list:
                self.image = pygame.transform.flip(img[0], self.left, False)
                self.causa_dano()
            else:
                self.image = pygame.transform.flip(img, self.left, False)
        elif self.walk:
            self.image = pygame.transform.flip(self.walk_animacao.__next__(), self.left, False)
        else:
            self.image = pygame.transform.flip(self.idle_animacao.__next__(), self.left, False)
