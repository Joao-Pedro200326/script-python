import os, sys

dirpath = os.getcwd()
sys.path.append(dirpath)

if getattr(sys, "frozen", False):
    os.chdir(sys._MEIPASS)

import pygame
import pickle
from random import randint
from threading import Thread

pygame.init()
pygame.font.init()
pygame.mixer.init()

os.environ['SDL_VIDEO_CENTERED'] = '1'

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

altura = 400
largura = 400
tilesize = 16

best = 0
var_som = True
var_musica = True

os.chdir(dirpath)
try:
    best, var_som, var_musica = pickle.load(open('save.save', 'rb'))
except FileNotFoundError:
    arq = open('save.save', 'wb+')
    arq.close()
except Exception as erro:
    print(erro)
finally:
    if getattr(sys, "frozen", False):
        os.chdir(sys._MEIPASS)

janela = pygame.display.set_mode((altura, largura), pygame.NOFRAME)


class Minhathread:
    def __init__(self, funcao, daemon):
        self.thread = Thread(target=lambda: self.alpha(funcao), daemon=daemon)
        self.vivo = True

    def start(self):
        self.thread.start()

    def kill(self):
        self.vivo = False

    def alpha(self, obj):
        ret = pygame.Surface((40, 40))
        ret.fill((20, 20, 20))
        tic = pygame.time.Clock()
        while True:
            tic.tick(200)
            janela.blit(ret, (0, 0))
            obj.luz()
            obj.blit(janela)
            pygame.display.update((0, 0, 40, 40))
            if not self.vivo:
                break


class Botaoluz:
    def __init__(self, imagem, minalpha, posicao, text=None, var=False):
        self.imagem = imagem.convert()
        self.imagem.set_alpha(minalpha)
        self.imagem.set_colorkey(self.imagem.get_at((0, 0)))
        self.alpha = minalpha
        self.posicao = posicao
        self.som = pygame.mixer.Sound('data/toque.ogg')
        self.var = var
        if text is not None:
            texto = pygame.font.SysFont('Times', 30).render(text, True, (0, 0, 0))
            self.imagem.blit(texto, (self.imagem.get_width() // 2 - texto.get_width() // 2,
                                     self.imagem.get_height() // 2 - texto.get_height() // 2))

    def troca_imagem(self, imagem):
        al = self.imagem.get_alpha()
        self.imagem = imagem.convert()
        self.imagem.set_alpha(al)
        self.imagem.set_colorkey(self.imagem.get_at((0, 0)))

    def run(self):
        return self.posicao[0] < pygame.mouse.get_pos()[0] < self.posicao[0] + self.imagem.get_width() \
               and self.posicao[1] < pygame.mouse.get_pos()[1] < self.posicao[1] + self.imagem.get_height()

    def luz(self, alpha_pulo=1):
        if self.posicao[0] < pygame.mouse.get_pos()[0] < self.posicao[0] + self.imagem.get_width() \
                and self.posicao[1] < pygame.mouse.get_pos()[1] < self.posicao[1] + self.imagem.get_height():
            self.imagem.set_alpha(self.imagem.get_alpha() + alpha_pulo)
        else:
            if self.imagem.get_alpha() > self.alpha:
                self.imagem.set_alpha(self.imagem.get_alpha() - alpha_pulo)

    def blit(self, superficie):
        superficie.blit(self.imagem, self.posicao)


class Botaopause:
    def __init__(self, sup, tamanho, tamanhomed, tamanhomax, pos):
        self.sup = sup
        self.sup_tr = pygame.transform.scale(sup, (tamanho, tamanho))
        self.tamanho = tamanho
        self.tamanhomedio = tamanhomed
        self.tamanhomax = tamanhomax
        self.pos = pos
        self.som = pygame.mixer.Sound('data/toque.ogg')

    def inicial_medio(self):
        if self.tamanho < self.tamanhomedio:
            self.tamanho += 1
            self.sup_tr = pygame.transform.scale(self.sup, (self.tamanho, self.tamanho))

    def medio_max(self):
        if self.pos[0] - self.tamanho // 2 < pygame.mouse.get_pos()[0] < self.pos[0] + self.tamanho // 2 \
                and self.pos[1] - self.tamanho // 2 < pygame.mouse.get_pos()[1] < self.pos[1] + self.tamanho // 2:
            if self.tamanho < self.tamanhomax:
                self.tamanho += 1
                self.sup_tr = pygame.transform.scale(self.sup, (self.tamanho, self.tamanho))
                return True
        else:
            if self.tamanho > self.tamanhomedio:
                self.tamanho -= 1
                self.sup_tr = pygame.transform.scale(self.sup, (self.tamanho, self.tamanho))
                return False

    def click(self):
        return self.pos[0] - self.tamanho // 2 < pygame.mouse.get_pos()[0] < self.pos[0] + self.tamanho // 2 \
                and self.pos[1] - self.tamanho // 2 < pygame.mouse.get_pos()[1] < self.pos[1] + self.tamanho // 2

    def desparecer(self):
        if self.tamanho > 1:
            self.tamanho -= 1
            self.sup_tr = pygame.transform.scale(self.sup, (self.tamanho, self.tamanho))


def sprite(image, linhas, colunas, size_x, size_y, convert=False):
    if convert:
        image.convert()
        image.set_colorkey(image.get_at((0, 0)))

    image_recurtada = []
    for y in range(0, linhas):
        linha = []
        for x in range(0, colunas):
            linha.append(image.subsurface(x * size_x, y * size_y, size_x, size_y))
        image_recurtada.append(linha)
    return image_recurtada


def alpha(obj):
    ret = pygame.Surface((40, 40))
    ret.fill((20, 20, 20))
    tic = pygame.time.Clock()
    while True:
        tic.tick(200)
        janela.blit(ret, (0, 0))
        obj.luz()
        obj.blit(janela)
        pygame.display.update((0, 0, 40, 40))


def colisao(objeto1, objeto_2):
    return objeto1[0] == objeto_2[0] and objeto1[1] == objeto_2[1]


def colisao_maca(objeto1, objeto1_2, objeto_2):
    return (objeto1[0] == objeto_2[0] and objeto1[1] == objeto_2[1]) \
           or (objeto1_2[0] == objeto_2[0] and objeto1_2[1] == objeto_2[1])


def maca_pos_al():
    x = randint(0, 19) * tilesize + 40
    y = randint(0, 19) * tilesize + 40
    return x, y


# <--------------------------------------------------menu-------------------------------------------------------------->


def menu():
    global best, var_som, var_musica

    pygame.mixer_music.load('data/menu_musica.mp3')

    defenicoes = sprite(pygame.image.load('data/menu_def.png'), 3, 2, 50, 50, True)
    bt_def = Botaoluz(defenicoes[0][1], 70, (175, 320))
    if var_som:
        bt_som = Botaoluz(defenicoes[2][0], 100, (175, 320))
    else:
        bt_som = Botaoluz(defenicoes[2][1], 100, (175, 320))
    if var_musica:
        bt_musica = Botaoluz(defenicoes[1][0], 100, (175, 320))
    else:
        bt_musica = Botaoluz(defenicoes[1][1], 100, (175, 320))

    if var_musica:
        pygame.mixer_music.play(-1)

    snake_titulo = pygame.font.SysFont('Times', 50).render('Snake', True, (200, 200, 200))
    melhor_pontuacao_titulo = pygame.font.SysFont('Times', 22).render('Melhor pontuação ', True, (150, 250, 150))

    iniciar = Botaoluz(pygame.image.load('data/iniciar.png'), 22, (10, 320), text='Iniciar')

    sair = Botaoluz(pygame.image.load('data/sair.png'), 22, (240, 320), text='Sair')

    while True:
        pygame.mouse.set_visible(True)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if iniciar.run():
                        if var_som:
                            iniciar.som.play()
                        game()
                        pygame.mixer_music.load('data/menu_musica.mp3')
                        pygame.mixer_music.play(-1)
                    elif sair.run():
                        return
                    elif bt_def.run():
                        if var_som:
                            bt_def.som.play()
                        if not bt_def.var:
                            bt_def.troca_imagem(defenicoes[0][0])
                        else:
                            bt_def.troca_imagem(defenicoes[0][1])
                        bt_def.var = not bt_def.var
                    elif bt_som.run():
                        var_som = not var_som
                        if var_som:
                            bt_som.som.play()
                        if var_som:
                            bt_som.troca_imagem(defenicoes[2][0])
                        else:
                            bt_som.troca_imagem(defenicoes[2][1])
                    elif bt_musica.run():
                        if var_som:
                            bt_musica.som.play()
                        var_musica = not var_musica
                        if var_musica:
                            bt_musica.troca_imagem(defenicoes[1][0])
                        else:
                            bt_musica.troca_imagem(defenicoes[1][1])

        iniciar.luz()
        sair.luz()

        if not (165 < pygame.mouse.get_pos()[0] < 235 and 210 < pygame.mouse.get_pos()[1] < 380):
            bt_def.var = False
            bt_def.troca_imagem(defenicoes[0][1])

        if bt_def.var:
            bt_musica.luz()
            bt_som.luz()
            if bt_som.posicao[1] > 270:
                bt_som.posicao = (bt_som.posicao[0], bt_som.posicao[1] - 1)
                bt_musica.posicao = (bt_musica.posicao[0], bt_musica.posicao[1] - 1)
            elif bt_musica.posicao[1] > 220:
                bt_musica.posicao = (bt_musica.posicao[0], bt_musica.posicao[1] - 1)
        elif not bt_def.var:
            bt_def.luz()
            if bt_som.posicao[1] < 320:
                bt_som.posicao = (bt_som.posicao[0], bt_som.posicao[1] + 1)
            if bt_musica.posicao[1] < 320:
                bt_musica.posicao = (bt_musica.posicao[0], bt_musica.posicao[1] + 1)

        if not var_musica:
            pygame.mixer_music.pause()
        else:
            pygame.mixer_music.unpause()

        janela.fill((20, 20, 20))

        janela.blit(snake_titulo, (largura // 2 - snake_titulo.get_size()[0] // 2, 50))
        janela.blit(melhor_pontuacao_titulo, (5 + largura // 2 - melhor_pontuacao_titulo.get_size()[0] // 2,
                                              65 + snake_titulo.get_size()[1]))

        melhor_pontuacao = pygame.font.SysFont('Times', 22).render(str(best), True, (150, 250, 150))
        janela.blit(melhor_pontuacao, (largura // 2 - melhor_pontuacao.get_size()[0] // 2,
                                       70 + snake_titulo.get_size()[1] + melhor_pontuacao_titulo.get_size()[1]))

        iniciar.blit(janela)

        sair.blit(janela)

        bt_musica.blit(janela)
        bt_som.blit(janela)
        a = pygame.Surface((50, 50))
        a.fill((20, 20, 20))
        janela.blit(a, (175, 320))
        bt_def.blit(janela)

        pygame.display.update()


# <----------------------------------------------------game------------------------------------------------------------>


def game():

    def gameover():
        gameover_rgb = (20, 20, 20)
        gameover_fontsize = 10
        superficie = pygame.Surface((400, 60))
        sub = janela.subsurface((0, 33, 400, 60))
        superficie.blit(sub, (0, 0))

        while gameover_rgb[0] < 255:
            gameover_rgb = (gameover_rgb[0] + 1, gameover_rgb[1] + 1, gameover_rgb[2] + 1)

            janela.blit(superficie, (0, 33))

            if gameover_fontsize < 60:
                gameover_fontsize += 1

            gameover_texto = pygame.font.SysFont('Times', gameover_fontsize).render('Gameover', True, gameover_rgb)
            janela.blit(gameover_texto, (200 - gameover_texto.get_size()[0] // 2, 33))
            pygame.display.update()
        pygame.display.update()
        pygame.mixer_music.fadeout(1500)
        pygame.time.wait(1500)
        return

    global best, var_som, var_musica

    pygame.mixer.music.load('data/musica.mp3')
    pygame.mixer.music.play(-1)

    if not var_musica:
        pygame.mixer_music.pause()

    snake = [(200, 200), (184, 200), (168, 200)]
    snake_skin = sprite(pygame.image.load('data/cobra_sprite-sheet.png'), 3, 3, tilesize, tilesize)
    direcao = RIGHT

    maca = pygame.image.load('data/maçã.png')
    maca_pos = maca_pos_al()
    maca_som = pygame.mixer.Sound('data/maçã.ogg')

    pause = Botaoluz(pygame.image.load('data/pause.png'), 22, (3, 3))
    pause_alpha = Minhathread(pause, True)
    pause_alpha.start()

    scoore = 0

    relogio = pygame.time.Clock()
    pygame.mouse.set_visible(False)

    while True:
        relogio.tick(7)

        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if pause.run():
                        if var_som:
                            pause.som.play()
                        pause_alpha.kill()
                        del pause_alpha
                        if pausem():
                            if scoore > best:
                                best = scoore
                            return
                        else:
                            pause_alpha = Minhathread(pause, True)
                            pause_alpha.start()
                            relogio.tick(7)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if var_som:
                        pause.som.play()
                    pause_alpha.kill()
                    del pause_alpha
                    if pausem():
                        if scoore > best:
                            best = scoore
                        return
                    else:
                        pause_alpha = Minhathread(pause, True)
                        pause_alpha.start()
                        relogio.tick(7)
                if event.key == pygame.K_UP and direcao != DOWN:
                    direcao = UP
                    break
                if event.key == pygame.K_DOWN and direcao != UP:
                    direcao = DOWN
                    break
                if event.key == pygame.K_RIGHT and direcao != LEFT:
                    direcao = RIGHT
                    break
                if event.key == pygame.K_LEFT and direcao != RIGHT:
                    direcao = LEFT
                    break

        if colisao_maca(snake[0], snake[1], maca_pos):
            if var_som:
                maca_som.play()
            maca_pos = maca_pos_al()
            while maca_pos in snake:
                maca_pos = maca_pos_al()
            scoore += 1
            snake.append((0, 0))
            pygame.time.wait(20)

        for parte in range(len(snake) - 1, 0, -1):
            snake[parte] = (snake[parte - 1][0], snake[parte - 1][1])

        if direcao == UP:
            snake[0] = (snake[0][0], snake[0][1] - tilesize)
            if snake[0][1] < 40:
                snake[0] = (snake[0][0], 400 - 40 - tilesize)
        elif direcao == DOWN:
            snake[0] = (snake[0][0], snake[0][1] + tilesize)
            if snake[0][1] > 40 + tilesize * 19:
                snake[0] = (snake[0][0], 40)
        elif direcao == RIGHT:
            snake[0] = (snake[0][0] + tilesize, snake[0][1])
            if snake[0][0] > 40 + tilesize * 19:
                snake[0] = (40, snake[0][1])
        elif direcao == LEFT:
            snake[0] = (snake[0][0] - tilesize, snake[0][1])
            if snake[0][0] < 40:
                snake[0] = (400 - 40 - tilesize, snake[0][1])
        if pygame.mouse.get_pos()[0] < 40 or pygame.mouse.get_pos()[0] > 360 or \
                pygame.mouse.get_pos()[1] < 40 or pygame.mouse.get_pos()[1] > 360:
            pygame.mouse.set_visible(True)
        else:
            pygame.mouse.set_visible(False)

        # <----------------------------------------------blit---------------------------------------------------------->

        janela.fill((20, 20, 20))

        pause.blit(janela)

        for parte in range(len(snake) - 1, -1, -1):
            if parte == 0:
                if direcao == RIGHT:
                    janela.blit(pygame.transform.rotate(snake_skin[0][0], 270), snake[parte])
                elif direcao == LEFT:
                    janela.blit(pygame.transform.rotate(snake_skin[0][0], 90), snake[parte])
                elif direcao == DOWN:
                    janela.blit(pygame.transform.rotate(snake_skin[0][0], 180), snake[parte])
                else:
                    janela.blit(snake_skin[0][0], snake[parte])
            elif parte == len(snake) - 1:
                if snake[parte - 1][0] > snake[parte][0]:
                    janela.blit(pygame.transform.rotate(snake_skin[1][0], 270), snake[parte])
                elif snake[parte - 1][0] < snake[parte][0]:
                    janela.blit(pygame.transform.rotate(snake_skin[1][0], 90), snake[parte])
                elif snake[parte - 1][1] > snake[parte][1]:
                    janela.blit(pygame.transform.rotate(snake_skin[1][0], 180), snake[parte])
                else:
                    janela.blit(snake_skin[1][0], snake[parte])
            else:
                if ((snake[parte + 1][0] == snake[parte][0] - tilesize
                     and snake[parte][1] - tilesize == snake[parte - 1][1])
                    or (snake[parte + 1][0] == 40 + 19 * tilesize and snake[parte][0] == 40
                        and snake[parte - 1][1] == snake[parte][1] - tilesize)
                    or (snake[parte + 1][0] == snake[parte][0] - tilesize and snake[parte][1] == 40
                        and snake[parte - 1][1] == 40 + 19 * tilesize)
                    or (snake[parte + 1] == (40 + 19 * tilesize, 40)
                        and snake[parte] == (40, 40) and snake[parte - 1] == (40, 40 + 19 * tilesize))) \
                        or ((snake[parte + 1][1] == snake[parte][1] - tilesize
                             and snake[parte][0] - tilesize == snake[parte - 1][0])
                            or (snake[parte + 1][1] == 40 + 19 * tilesize
                                and snake[parte][1] == 40 and snake[parte - 1][0] == snake[parte][0] - tilesize)
                            or (snake[parte + 1][1] == snake[parte][1] - tilesize and snake[parte][0] == 40
                                and snake[parte - 1][0] == 40 + 19 * tilesize)
                            or (snake[parte + 1] == (40, 40 + 19 * tilesize)
                                and snake[parte] == (40, 40) and snake[parte - 1] == (40 + 19 * tilesize, 40))):
                    janela.blit(snake_skin[1][1], snake[parte])

                elif ((snake[parte + 1][0] == snake[parte][0] - tilesize
                       and snake[parte][1] + tilesize == snake[parte - 1][1])
                      or (snake[parte + 1][0] == 40 + 19 * tilesize and snake[parte][0] == 40
                          and snake[parte - 1][1] == snake[parte][1] + tilesize)
                      or (snake[parte + 1][0] == snake[parte][0] - tilesize and snake[parte][1] == 40 + 19 * tilesize
                          and snake[parte - 1][1] == 40)
                      or (snake[parte + 1] == (40 + 19 * tilesize, 40 + 19 * tilesize)
                          and snake[parte] == (40, 40 + 19 * tilesize) and snake[parte - 1] == (40, 40))) \
                        or ((snake[parte + 1][1] == snake[parte][1] + tilesize
                             and snake[parte][0] - tilesize == snake[parte - 1][0])
                            or (snake[parte + 1][1] == 40 and snake[parte][1] == 40 + 19 * tilesize
                                and snake[parte - 1][0] == snake[parte][0] - tilesize)
                            or (snake[parte + 1][1] == snake[parte][1] + tilesize and snake[parte][0] == 40
                                and snake[parte - 1][0] == 40 + 19 * tilesize)
                            or (snake[parte + 1] == (40, 40)
                                and snake[parte] == (40, 40 + 19 * tilesize)
                                and snake[parte - 1] == (40 + 19 * tilesize, 40 + 19 * tilesize))):
                    janela.blit(snake_skin[2][1], snake[parte])

                elif ((snake[parte + 1][0] == snake[parte][0] + tilesize
                       and snake[parte][1] - tilesize == snake[parte - 1][1])
                      or (snake[parte + 1][0] == 40 and snake[parte][0] == 40 + 19 * tilesize
                          and snake[parte - 1][1] == snake[parte][1] - tilesize)
                      or (snake[parte + 1][0] == snake[parte][0] + tilesize and snake[parte][1] == 40
                          and snake[parte - 1][1] == 40 + 19 * tilesize)
                      or (snake[parte + 1] == (40, 40) and snake[parte] == (40 + 19 * tilesize, 40)
                          and snake[parte - 1] == (40 + 19 * tilesize, 40 + 19 * tilesize))) \
                        or ((snake[parte + 1][1] == snake[parte][1] - tilesize
                             and snake[parte][0] + tilesize == snake[parte - 1][0])
                            or (snake[parte + 1][1] == 40 + 19 * tilesize and snake[parte][1] == 40
                                and snake[parte - 1][0] == snake[parte][0] + tilesize)
                            or (snake[parte + 1][1] == snake[parte][1] - tilesize
                                and snake[parte][0] == 40 + 19 * tilesize
                                and snake[parte - 1][0] == 40)
                            or (snake[parte + 1] == (40 + 19 * tilesize, 40 + 19 * tilesize)
                                and snake[parte] == (40 + 19 * tilesize, 40)
                                and snake[parte - 1] == (40, 40))):
                    janela.blit(snake_skin[1][2], snake[parte])

                elif ((snake[parte + 1][0] == snake[parte][0] + tilesize
                       and snake[parte][1] + tilesize == snake[parte - 1][1])
                      or (snake[parte + 1][0] == 40 and snake[parte][0] == 40 + 19 * tilesize
                          and snake[parte - 1][1] == snake[parte][1] + tilesize)
                      or (snake[parte + 1][0] == snake[parte][0] + tilesize and snake[parte][1] == 40 + 19 * tilesize
                          and snake[parte - 1][1] == 40)
                      or (snake[parte + 1] == (40, 40 + 19 * tilesize)
                          and snake[parte] == (40 + 19 * tilesize, 40 + 19 * tilesize)
                          and snake[parte - 1] == (40 + 19 * tilesize, 40))) \
                        or ((snake[parte + 1][1] == snake[parte][1] + tilesize
                             and snake[parte][0] + tilesize == snake[parte - 1][0])
                            or (snake[parte + 1][1] == 40 and snake[parte][1] == 40 + 19 * tilesize
                                and snake[parte - 1][0] == snake[parte][0] + tilesize)
                            or (snake[parte + 1][1] == snake[parte][1] + tilesize
                                and snake[parte][0] == 40 + 19 * tilesize
                                and snake[parte - 1][0] == 40)
                            or (snake[parte + 1] == (40 + 19 * tilesize, 40)
                                and snake[parte] == (40 + 19 * tilesize, 40 + 19 * tilesize)
                                and snake[parte - 1] == (40, 40 + 19 * tilesize))):
                    janela.blit(snake_skin[2][0], snake[parte])

                else:
                    if parte % 2 == 0:
                        if snake[parte + 1][1] == snake[parte][1] == snake[parte - 1][1]:
                            janela.blit(pygame.transform.rotate(snake_skin[0][1], 90), snake[parte])
                        else:
                            janela.blit(snake_skin[0][1], snake[parte])
                    else:
                        if snake[parte + 1][1] == snake[parte][1] == snake[parte - 1][1]:
                            janela.blit(pygame.transform.rotate(snake_skin[0][2], 90), snake[parte])
                        else:
                            janela.blit(snake_skin[0][2], snake[parte])

        pontuacao = pygame.font.SysFont('Times', 20).render('Pontuação ' + str(scoore), True, (100, 250, 120))

        janela.blit(maca, maca_pos)

        pygame.draw.line(janela, (255, 255, 255), (40, 40), (40, 40 + 20 * tilesize))
        pygame.draw.line(janela, (255, 255, 255), (40, 40 + 20 * tilesize), (40 + 20 * tilesize, 40 + 20 * tilesize))
        pygame.draw.line(janela, (255, 255, 255), (40 + 20 * tilesize, 40 + 20 * tilesize), (40 + 20 * tilesize, 40))
        pygame.draw.line(janela, (255, 255, 255), (40 + 20 * tilesize, 40), (40, 40))

        janela.blit(pontuacao, (150, 10))

        for parte in range(1, len(snake)):
            if colisao(snake[0], snake[parte]):
                gameover()
                if scoore > best:
                    best = scoore
                janela.fill((20, 20, 20))
                pause_alpha.kill()
                return

        pygame.display.update()


# <------------------------------------------------pausa--------------------------------------------------------------->


def pausem():
    global var_som, var_musica
    pausa_text = pygame.font.SysFont('Times', 60).render('Pausa', True, (200, 200, 200))

    pygame.mouse.set_visible(True)

    menu_pause = sprite(pygame.image.load('data/pause_menu.png'), 3, 2, 100, 100)

    superficie = pygame.Surface((400, 400))
    sub = janela.subsurface((0, 0, 400, 400))
    superficie.blit(sub, (0, 0))

    fundo = pygame.Surface((400, 400))
    fundo.fill((0, 0, 0))
    fundo.convert()
    fundo.set_alpha(1)

    text = [('', ''), ('', '')]
    texto_pause = pygame.font.SysFont('Times', 40).render(text[1][1], True, (200, 200, 200))

    troca_de_botoes = pygame.mixer.Sound('data/troca.ogg')
    canal = troca_de_botoes.play()
    canal.stop()

    volta = Botaopause(menu_pause[0][0], 1, 80, 100, (50, 150))
    if var_musica:
        musica = Botaopause(menu_pause[1][0], 1, 80, 100, (150, 150))
    else:
        musica = Botaopause(menu_pause[1][1], 1, 80, 100, (150, 150))
    if var_som:
        som = Botaopause(menu_pause[2][0], 1, 80, 100, (250, 150))
    else:
        som = Botaopause(menu_pause[2][1], 1, 80, 100, (250, 150))
    sair = Botaopause(menu_pause[0][1], 1, 80, 100, (350, 150))

    relogio = pygame.time.Clock()

    def retorno():
        while volta.tamanho > 1:
            pygame.event.get()

            sair.desparecer()
            if sair.tamanho < 50:
                som.desparecer()
            if som.tamanho < 50:
                musica.desparecer()
            if musica.tamanho < 50:
                volta.desparecer()
            if fundo.get_alpha() > 0:
                fundo.set_alpha(fundo.get_alpha() - 1)

            janela.blit(superficie, (0, 0))
            janela.blit(fundo, (0, 0))

            janela.blit(volta.sup_tr, (50 - volta.tamanho // 2, 150 - volta.tamanho // 2))
            janela.blit(musica.sup_tr, (150 - musica.tamanho // 2, 150 - musica.tamanho // 2))
            janela.blit(som.sup_tr, (250 - som.tamanho // 2, 150 - som.tamanho // 2))
            janela.blit(sair.sup_tr, (350 - sair.tamanho // 2, 150 - sair.tamanho // 2))

            pygame.display.update()
        pygame.time.wait(100)

    def texto():
        sup = pygame.Surface((400, 100))
        sup.blit(superficie.subsurface((0, 310, 400, 90)), (0, 0))
        sup.blit(fundo, (0, 0))
        frase = pygame.font.SysFont('Times', 40).render(text[1][1], True, (200, 200, 200))
        sup.blit(frase, (200 - frase.get_width() // 2, 0))
        sup.convert()
        sup.set_alpha(255)
        return sup
    
    def inicio():
        while sair.tamanho != sair.tamanhomedio:
            for event in pygame.event.get():
                pass
            volta.inicial_medio()
            if volta.tamanho > 50:
                musica.inicial_medio()
            if musica.tamanho > 50:
                som.inicial_medio()
            if som.tamanho > 50:
                sair.inicial_medio()
            if fundo.get_alpha() < 200:
                fundo.set_alpha(fundo.get_alpha() + 1)

            janela.blit(superficie, (0, 0))
            janela.blit(fundo, (0, 0))
            janela.blit(pausa_text, (200 - pausa_text.get_size()[0] // 2, 15))

            janela.blit(volta.sup_tr, (50 - volta.tamanho // 2, 150 - volta.tamanho // 2))
            janela.blit(musica.sup_tr, (150 - musica.tamanho // 2, 150 - musica.tamanho // 2))
            janela.blit(som.sup_tr, (250 - som.tamanho // 2, 150 - som.tamanho // 2))
            janela.blit(sair.sup_tr, (350 - sair.tamanho // 2, 150 - sair.tamanho // 2))

            janela.blit(texto_pause, (0, 310))

            pygame.display.update()

    inicio()

    while True:
        relogio.tick(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if var_som:
                        volta.som.play()
                    retorno()
                    return
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    if volta.click():
                        if var_som:
                            volta.som.play()
                        retorno()
                        return
                    elif musica.click():
                        var_musica = not var_musica
                        musica.tamanho -= 5
                        if var_som:
                            musica.som.play()
                        if var_musica:
                            musica.sup = menu_pause[1][0]
                            pygame.mixer.music.unpause()
                        else:
                            musica.sup = menu_pause[1][1]
                            pygame.mixer.music.pause()
                    elif som.click():
                        var_som = not var_som
                        som.tamanho -= 5
                        if var_som:
                            som.som.play()
                            som.sup = menu_pause[2][0]
                        else:
                            som.sup = menu_pause[2][1]
                    elif sair.click():
                        if var_som:
                            sair.som.play()
                        return True

        if fundo.get_alpha() < 200:
            fundo.set_alpha(fundo.get_alpha() + 1)

        if volta.tamanho >= volta.tamanhomedio:
            if volta.medio_max():
                text[0] = text[1]
                text[1] = ('volta', 'Voltar ao jogo')
        if musica.tamanho >= musica.tamanhomedio:
            if musica.medio_max():
                text[0] = text[1]
                if var_musica:
                    text[1] = ('musica', 'Musica: Ligado')
                else:
                    text[1] = ('musica', 'Musica: Desligado')
        if som.tamanho >= som.tamanhomedio:
            if som.medio_max():
                text[0] = text[1]
                if var_som:
                    text[1] = ('som', 'Som: Ligado')
                else:
                    text[1] = ('som', 'Som: Desligado')
        if sair.tamanho >= sair.tamanhomedio:
            if sair.medio_max():
                text[0] = text[1]
                text[1] = ('sair', 'Voltar para o menu')

        if volta.click() or musica.click() or som.click() or sair.click():
            texto_pause = texto()
        else:
            if texto_pause.get_alpha() is not None:
                texto_pause.set_alpha(texto_pause.get_alpha() - 1)

        if text[0][0] != text[1][0]:
            if not canal.get_busy() and var_som:
                canal.play(troca_de_botoes)
            text[0] = text[1]

        janela.blit(superficie, (0, 0))
        janela.blit(fundo, (0, 0))
        janela.blit(pausa_text, (200 - pausa_text.get_size()[0] // 2, 15))

        janela.blit(volta.sup_tr, (50 - volta.tamanho // 2, 150 - volta.tamanho // 2))
        janela.blit(musica.sup_tr, (150 - musica.tamanho // 2, 150 - musica.tamanho // 2))
        janela.blit(som.sup_tr, (250 - som.tamanho // 2, 150 - som.tamanho // 2))
        janela.blit(sair.sup_tr, (350 - sair.tamanho // 2, 150 - sair.tamanho // 2))

        janela.blit(texto_pause, (0, 310))

        pygame.display.update()


menu()

os.chdir(dirpath)
with open('save.save', 'wb') as arq:
    pickle.dump([best, var_som, var_musica], arq)
