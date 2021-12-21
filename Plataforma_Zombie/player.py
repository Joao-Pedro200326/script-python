import pygame
from settings import *
from random import randint
from data.ninja.idle import gera_idle
from data.ninja.run import gera_run
from data.ninja.jump import gera_jump
from data.ninja.throw import gera_throw
from data.ninja.glide import gera_glide

vetor2D = pygame.math.Vector2


class Player(pygame.sprite.Sprite):
    def __init__(self, game, xtop, ytop):
        pygame.sprite.Sprite.__init__(self)
        self.game = game
        self.vida = 100
        self.image = pygame.image.load('data/ninja/idle/Idle__0.png')
        self.rect = self.image.get_rect()
        self.rect.topleft = (xtop, ytop)
        self.vel = self.acl = vetor2D()
        self.run = False
        self.left = False
        self.jumping = False
        self.throw = False
        self.glide = False
        self.idle = gera_idle.animacao()
        self.run_animacao = gera_run.animacao()
        self.jump_animacao = gera_jump.animacao()
        self.throw_animacao = gera_throw.animacao()
        self.glide_animacao = gera_glide.animacao()

    def nova_imagem(self, image):
        center = self.rect.center
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = center

    def jump(self):
        self.rect.y += 1
        colisao = pygame.sprite.spritecollide(self, self.game.plataformas, False)
        self.rect.y -= 1
        if colisao:
            self.vel.y = -22
            self.jump_animacao = gera_jump.animacao()
            self.jumping = True

    def colisao_tiles(self):
        colisao = pygame.sprite.spritecollide(self, self.game.plataformas, False)
        for col_tile in colisao:
            if col_tile.rect.top < self.rect.bottom < col_tile.rect.bottom:
                self.rect.bottom = col_tile.rect.top + 1
                if self.vel.y - self.acl.y != -22:
                    self.vel.y = 0
                    self.jumping = False
                    self.glide = False
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

    def update(self):
        if self.vida < 0:
            self.kill()
        self.run = False
        self.acl = vetor2D(0, GRAVIDADE)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_e]:
            if not self.throw:
                self.throw = True
        elif keys[pygame.K_a]:
            self.acl.x = -PLAYER_ACL
            self.run = True
            if not self.left:
                self.left = True
        elif keys[pygame.K_d]:
            self.acl.x = PLAYER_ACL
            self.run = True
            if self.left:
                self.left = False

        self.acl.x += self.vel.x * PLAYER_ATR
        self.vel += self.acl
        if 0 > self.vel.x > -0.4:
            self.vel.x = 0
            self.acl = vetor2D(0, GRAVIDADE)
        self.colisao_tiles()
        self.rect.center += self.vel + 0.5 * self.acl

        if self.jumping:
            self.nova_imagem(pygame.transform.flip(self.jump_animacao.__next__(), self.left, False))
        elif self.throw:
            try:
                image = self.throw_animacao.__next__()
                if type(image) == list:
                    self.nova_imagem(pygame.transform.flip(image[0], self.left, False))
                    kunai = Kunai(self.rect.left, self.rect.center[1], self.game.mapa_size[0], self.left)
                    self.game.sprites.add(kunai)
                    self.game.kunais.add(kunai)
                else:
                    self.nova_imagem(pygame.transform.flip(image, self.left, False))
            except StopIteration:
                self.throw = False
                self.throw_animacao = gera_throw.animacao()
        elif self.glide:
            self.vel.y = 1.5
            self.vel.x = self.vel.x - self.acl.x
            if self.vel.x < 0:
                self.nova_imagem(pygame.transform.flip(self.glide_animacao.__next__(), True, False))
            else:
                self.nova_imagem(self.glide_animacao.__next__())
        elif self.run:
            self.nova_imagem(pygame.transform.flip(self.run_animacao.__next__(), self.left, False))
        else:
            self.nova_imagem(pygame.transform.flip(self.idle.__next__(), self.left, False))


class Kunai(pygame.sprite.Sprite):
    def __init__(self, x, y, x_max, left=False):
        pygame.sprite.Sprite.__init__(self)
        if left:
            self.vel_x = -30
            self.image = pygame.transform.flip(pygame.image.load('data/ninja/Kunai.png'), True, False)
        else:
            self.vel_x = 30
            self.image = pygame.image.load('data/ninja/Kunai.png')
            x += 100
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y + randint(-20, 20))
        self.x_max = x_max
        self.dano = 30

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.x > self.x_max or self.rect.x < -10:
            self.kill()
