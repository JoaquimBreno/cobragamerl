import pygame
import random
from enum import Enum
from collections import namedtuple


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
        self.velocidade = 10
        self.temp_velocidade = 0
        self.d = 0
        self.largura = largura
        self.altura = altura
        # tela
        self.display = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption('Cobra')
        self.clock = pygame.time.Clock()

        # inicia o estado do jogo
        self.direcao = Direcao.RIGHT

        self.cabeca = Point(self.largura/2, self.altura/2)
        self.cobra = [self.cabeca,
                      Point(self.cabeca.x-TAM_CAIXA, self.cabeca.y),
                      Point(self.cabeca.x-(2*TAM_CAIXA), self.cabeca.y)]
        self.pontuacao = 0
        self.maca = None
        self.set_maca()

    def set_maca(self):
        x = random.randint(0, (self.largura-TAM_CAIXA)//TAM_CAIXA)*TAM_CAIXA
        y = random.randint(0, (self.altura-TAM_CAIXA)//TAM_CAIXA)*TAM_CAIXA

        self.maca = Point(x, y)
        if self.maca in self.cobra:
            self.set_maca()

    def playloop(self):
        # Coletar entradas
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direcao = Direcao.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direcao = Direcao.RIGHT
                elif event.key == pygame.K_UP:
                    self.direcao = Direcao.UP
                elif event.key == pygame.K_DOWN:
                    self.direcao = Direcao.DOWN
        # Movimentos
        self.move(self.direcao)
        self.cobra.insert(0, self.cabeca)
        # Checa game over
        game_over = False
        if self.colisao():
            game_over = True
            return game_over, self.pontuacao
            
        # Adiciona maca ou movimenta
        if self.cabeca == self.maca:
            self.pontuacao += 1
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
        return game_over, self.pontuacao

    def colisao(self):
        if self.cabeca in self.cobra[1:]:
            return True        
        elif self.cabeca.x > self.largura - TAM_CAIXA:
            self.cabeca = Point(-20, self.cabeca.y)   
        elif self.cabeca.x < 0:
            self.cabeca = Point(640, self.cabeca.y)    
        elif self.cabeca.y >  self.altura - TAM_CAIXA:
            self.cabeca = Point(self.cabeca.x, -20)
        elif self.cabeca.y <  0:
            self.cabeca = Point(self.cabeca.x, 480)
        return False

    def atualiza_ui(self):
        self.display.fill(BLACK)

        for pt in self.cobra:
            pygame.draw.rect(self.display, VERDE, pygame.Rect(pt.x, pt.y, TAM_CAIXA, TAM_CAIXA))
        pygame.draw.rect(self.display, VERMELHO, pygame.Rect(self.maca.x, self.maca.y, TAM_CAIXA, TAM_CAIXA))

        text = font.render("Pontuação: " + str(self.pontuacao), True, BRANCO)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def move(self, direcao):
        x = self.cabeca.x
        y = self.cabeca.y
        # Verifica tecla e movimento anterior
        if direcao == Direcao.RIGHT and self.d!=2:
            self.d=1
        elif direcao == Direcao.LEFT and self.d!=1:
            self.d=2
        elif direcao == Direcao.DOWN and self.d!=4:
            self.d=3
        elif direcao == Direcao.UP and self.d!=3:
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

if __name__ == '__main__':

    game = JogoDaCobra()

    while True:
        game_over,pontuacao = game.playloop()
        if game_over == True:
            break
    print('Pontuação final: ', pontuacao)