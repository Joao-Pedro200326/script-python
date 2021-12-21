import pygame
from settings import *
from player import Player
from plataforma import Plataforma
from camara import Camara, Mapa
from mob import Mobmale


class Game:
    def __init__(self):
        pygame.init()
        self.janela = pygame.display.set_mode((largura, altura))
        self.gameloop = True
        self.sprites = pygame.sprite.Group()
        self.plataformas = pygame.sprite.Group()
        self.mobs = pygame.sprite.Group()
        self.kunais = pygame.sprite.Group()
        self.relogio = pygame.time.Clock()
        self.camara = Camara(largura, altura)
        self.player = None
        self.bg = pygame.transform.scale(pygame.image.load('data/cenario/bg.png'), (largura, altura))
        self.mapa_size = 0
        self.carregar_mapa()

    def carregar_mapa(self):
        for y, linha in enumerate(Mapa().mapa):
            for x, c in enumerate(linha):
                if c == 'P':
                    self.player = Player(self, x*tilesize, y*tilesize)
                    self.sprites.add(self.player)
                elif c == 'M':
                    mob = Mobmale(x*tilesize, y*tilesize, self)
                    self.sprites.add(mob)
                    self.mobs.add(mob)
                elif c != ' ':
                    p = Plataforma(x, y, c)
                    self.sprites.add(p)
                    self.plataformas.add(p)
        self.mapa_size = Mapa().size

    def run(self):
        while self.gameloop:
            self.relogio.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.gameloop = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.jump()
                if event.key == pygame.K_q:
                    self.player.glide = not self.player.glide

        colisao = pygame.sprite.groupcollide(self.kunais, self.mobs, True, False)
        if colisao:
            for k in colisao.keys():
                for sprite in colisao[k]:
                    sprite.dano(k.dano)

    def update(self):
        self.sprites.update()
        self.camara.update(self.player, Mapa().size)

    def draw(self):
        self.janela.fill((0, 0, 0))
        self.janela.blit(self.bg, (0, 0))
        for sprite in self.sprites:
            self.janela.blit(sprite.image, self.camara.apply(sprite))
        pygame.display.update()


g = Game()
g.run()
