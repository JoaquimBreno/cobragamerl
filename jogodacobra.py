import pygame
import random
from enum import Enum
from collections import namedtuple
import numpy as np


pygame.init()

font = pygame.font.Font('arial.ttf', 16)

#reset

# Recompensa

# Ação -> Direção

# Interação com o jogo

# Colisão
class Direcao(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4

Point = namedtuple('Point', 'x, y')
TAM_CAIXA = 20
BLACK = (0,0,0)
BRANCO = (255,255,255)
VERDE = (0,255,0)
VERMELHO = (255,0,0)

class JogoDaCobra:

    def __init__(self, largura = 640, altura = 480):
        self.velocidade = 15
        self.temp_velocidade = 0
        self.d = 0
        self.largura = largura
        self.altura = altura
        # tela
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Cobra')
        self.clock = pygame.time.Clock()
        self.resetar()

        # inicia o estado do jogo
    def resetar(self):
        self.direcao = Direcao.RIGHT

        self.cabeca = Point(self.largura/2, self.altura/2)
        self.cobra = [self.cabeca,
                      Point(self.cabeca.x-TAM_CAIXA, self.cabeca.y),
                      Point(self.cabeca.x-(2*TAM_CAIXA), self.cabeca.y)]
        self.pontuacao = 0
        self.maca = None
        self.set_maca()
        self.frame_interation

    def set_maca(self):
        x = random.randint(0, (self.largura-TAM_CAIXA)//TAM_CAIXA)*TAM_CAIXA
        y = random.randint(0, (self.altura-TAM_CAIXA)//TAM_CAIXA)*TAM_CAIXA

        self.maca = Point(x, y)
        if self.maca in self.cobra:
            self.set_maca()

    def playloop(self, acao):
        self.frame_interation += 1
        # Coletar entradas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
        # Movimentos
        self.move(acao)
        self.cobra.insert(0, self.cabeca)
        # Checa game over
        recompensa = 0
        game_over = False
        if self.colisao() or self.frame_interation > 100*len(self.snake):
            game_over = True
            recompensa = -10
            return recompensa, game_over, self.pontuacao
            
        # Adiciona maca ou movimenta
        if self.cabeca == self.maca:
            self.pontuacao += 1
            reward = 10
            # A cada 10 pontos adiciona uma velocidade
            if (self.pontuacao-self.temp_velocidade) == 10:
                self.temp_velocidade = self.pontuacao
                self.velocidade += 1
            self.set_maca()
        else:
            self.cobra.pop()

        # Atualiza tempo e interface
        self.atualiza_ui()
        self.clock.tick(self.velocidade)

        # Retorna game over e pontuacao
        return reward, game_over, self.pontuacao

    def colisao(self, cb = None):
        if cb is None:
            cb = self.cabeca
        if self.cb in self.cobra[1:]:
            return True        
        elif self.cb.x > self.largura - TAM_CAIXA:
            self.cb = Point(-20, self.cb.y)   
        elif self.cb.x < 0:
            self.cb = Point(640, self.cb.y)    
        elif self.cb.y >  self.altura - TAM_CAIXA:
            self.cb = Point(self.cb.x, -20)
        elif self.cb.y <  0:
            self.cb = Point(self.cb.x, 480)
        return False

    def atualiza_ui(self):
        self.display.fill(BLACK)

        for cb in self.cobra:
            pygame.draw.rect(self.display, VERDE, pygame.Rect(cb.x, cb.y, TAM_CAIXA, TAM_CAIXA))
        pygame.draw.rect(self.display, VERMELHO, pygame.Rect(self.maca.x, self.maca.y, TAM_CAIXA, TAM_CAIXA))

        text = font.render("Pontuação: " + str(self.pontuacao), True, BRANCO)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move(self, acao):

        sent_horario = [Direcao.RIGHT,Direcao.DOWN, Direcao.LEFT, Direcao.UP]
        idx = sent_horario.index(self.direcao)

        if np.array_equal(acao, [1,0,0]):
            nova_dir = clock_wise[idx]
        if np.array_equal(acao, [0,1,0]):
            next_idx = (idx + 1) % 4
            nova_dir = sent_horario[next_idx]
        else:
            next_idx = (idx - 1) % 4
            nova_dir = sent_horario[next_idx]
        
        self.direcao = new_dir

        x = self.cabeca.x
        y = self.cabeca.y
        # Verifica tecla e movimento anterior
        if self.direcao == Direcao.RIGHT and self.d!=2:
            self.d=1
        elif self.direcao == Direcao.LEFT and self.d!=1:
            self.d=2
        elif self.direcao == Direcao.DOWN and self.d!=4:
            self.d=3
        elif self.direcao == Direcao.UP and self.d!=3:
            self.d=4

        #Executa movimento
        if self.d==1:
            x+= TAM_CAIXA
        elif self.d==2:
            x-= TAM_CAIXA 
        elif self.d==3:
            y+= TAM_CAIXA
        elif self.d==4:
            y-= TAM_CAIXA

        self.cabeca = Point(x,y)
