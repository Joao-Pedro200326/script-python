import pygame
from pygame import *
from variaveis import *
from player import Player, Camara


class Game():
    def __init__(self):
        global RESUL
        pygame.init()
        RESUL = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        self.janela = pygame.display.set_mode(RESUL, FULLSCREEN, 32)
        pygame.display.set_caption('Nosso jogo')
        self.display = pygame.Surface(RESUL_BASE)
        self.surf_mapa = pygame.image.load('img/Sem Título.png')
        self.camara = Camara(RESUL_BASE)

        self.all_sprites = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        
        self.relogio = pygame.time.Clock()
        self.gameloop = 1
        self.run()

    def run(self):
        while self.gameloop:
            self.relogio.tick(FPS)
            self.events()
            self.updating()
            self.drawing()
    
    def events(self):
        for event in pygame.event.get():
            if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                self.gameloop = 0

    def updating(self):
        self.all_sprites.update()

    def drawing(self):
        self.surf_mapa = pygame.image.load('img/Sem Título.png')
        self.all_sprites.draw(self.surf_mapa)
        self.display.blit(self.camara.draw(self.player, self.surf_mapa), (0,0))
        self.janela.blit(pygame.transform.scale(self.display, RESUL), (0,0))
        pygame.display.update()


Game()