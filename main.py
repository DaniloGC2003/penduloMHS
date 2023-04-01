import pygame
import math

UM_METRO = 1000  # 1000 pixels
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
POS_INICIAL = (400, 50)  # posicao do fio
ACELERACAO_GRAVIDADE = 9.8
MILISEGUNDO_PARA_SEGUNDO = 1000 #fator de conversao
CLICOU = 1
NAO_CLICOU = 0


class Botao:

    def __init__(self, pos, size, text, unselectedColor, selectedColor):
        super().__init__()
        self.pos = pos
        self.size = size
        self.text = text #string
        self.font = pygame.font.Font(None, 80)
        self.textSurface = self.font.render(text, True, (0, 0, 0))
        self.unselectedColor = unselectedColor
        self.selectedColor = selectedColor

        self.currentColor = self.unselectedColor
        self.selected = False
        self.clicked = False

    def checkHovering(self):#verifica se o mouse se encontra sobre o botao
        mousePos = pygame.mouse.get_pos()
        if (mousePos[0] > self.pos[0] and mousePos[0] < self.pos[0] + self.size[0]) and (mousePos[1] > self.pos[1] and mousePos[1] < self.pos[1] + self.size[1]):
            return True
        return False

    def exec(self, window):#funcao principal de acao do botao. verifica cliques e se desenha na tela
        clicou = False
        if self.checkHovering():
            self.currentColor = self.selectedColor
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                clicou = True
                self.clicked = True
            if pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        else:
            self.currentColor = self.unselectedColor
            self.clicked = False

        pygame.draw.rect(window, (0, 0, 0), [
                         self.pos[0], self.pos[1], self.size[0], self.size[1]])
        pygame.draw.rect(window, self.currentColor, [
                         self.pos[0] + 5, self.pos[1] + 5, self.size[0] - 10, self.size[1] - 10])
        window.blit(self.textSurface, (self.pos[0] + 65, self.pos[1] + 25))

        return clicou


class BotaoDeslizante:
    def __init__(self, pos, text, unselectedColor, selectedColor, min, max):
        self.pos = pos
        self.size = (300, 10)
        self.text = text
        self.font = pygame.font.Font(None, 40)

        self.unselectedColor = unselectedColor
        self.selectedColor = selectedColor
        self.currentColor = unselectedColor

        self.currentValue = min

        self.buttonPos = [self.pos[0], self.pos[1] + 5]
        self.buttonRadius = 15

        self.textSurface = self.font.render(text, True, (0, 0, 0))

        self.min = min
        self.max = max

    def checkHovering(self):#verifica se o mouse se encontra sobre o botao
        mousePos = pygame.mouse.get_pos()
        if math.sqrt((self.buttonPos[0] - mousePos[0])**2 + (self.buttonPos[1] - mousePos[1])**2) < self.buttonRadius:
            return True
        return False

    def map_range(self, x, in_min, in_max, out_min, out_max):#mapeia um intervalo a outro de forma linear
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def exec(self, window):#funcao principal
        if self.checkHovering():#acao no caso em que o botao eh clicado
            self.currentColor = self.selectedColor
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        elif pygame.mouse.get_pressed()[0] == 0:
            self.currentColor = self.unselectedColor
            self.clicked = False

        if self.clicked == True and pygame.mouse.get_pos()[0] > self.pos[0] and pygame.mouse.get_pos()[0] < self.pos[0] + self.size[0]:#arrastar o botao
            self.buttonPos[0] = pygame.mouse.get_pos()[0]

        #desenhar o botao
        pygame.draw.rect(window, (115, 115, 115), [
                         self.pos[0], self.pos[1], self.size[0], self.size[1]])
        pygame.draw.circle(
            window, (0, 0, 0), (self.buttonPos[0], self.buttonPos[1]), self.buttonRadius)
        pygame.draw.circle(window, self.currentColor,
                           (self.buttonPos[0], self.buttonPos[1]), self.buttonRadius - 4)
        self.currentValue = self.map_range(
            self.buttonPos[0], self.pos[0], self.pos[0] + self.size[0], self.min, self.max)
        message = self.text + ': ' + str(round(self.currentValue, 3))
        self.textSurface = self.font.render(message, True, (0, 0, 0))
        window.blit(self.textSurface, (self.pos[0] - 20, self.pos[1] + 25))


class GUI:  # controle de parametros do pendulo
    def __init__(self):
        self.enterButton = Botao(
            (WINDOW_WIDTH - 400 + 50, 650), (300, 100), 'Enter', (112, 250, 37), (76, 168, 25))
        self.comprimentoPendulo = BotaoDeslizante(
            (WINDOW_WIDTH - 400 + 50, 300), 'Comprimento (m)', (7, 242, 70), (3, 163, 46), 0.01, 0.7)
        self.amplitudePendulo = BotaoDeslizante(
            (WINDOW_WIDTH - 400 + 50, 500), 'Amplitude (rad)', (7, 242, 70), (3, 163, 46), 0.01, 0.5)
        
        self.font = pygame.font.Font(None, 35)
        self.textoLinha1 = 'Utilize os botões para alterar'
        self.textoLinha2 = 'os parâmetros do pêndulo'
        self.texto1Surface = self.font.render(self.textoLinha1, True, (0, 0, 0))
        self.texto2Surface = self.font.render(self.textoLinha2, True, (0, 0, 0))
        self.energiacineticaSurface = self.font.render('0', True, (0, 0, 0))
        self.energiapotencialSurface = self.font.render('0', True, (0, 0, 0))
        self.zeroSurface = self.font.render('0 J', True, (0, 0, 0))
        self.energiaMaxSurface = self.font.render('0', True, (0, 0, 0))

    def map_range(self, x, in_min, in_max, out_min, out_max):#mapeia um intervalo a outro de forma linear
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def exec(self, window, energiacinetica, energiapotencial, energiaMax):#desenha elementos na tela; chama funcao exec de seus objetos
        pygame.draw.rect(window, (0, 0, 0), [WINDOW_WIDTH - 400, 5, 395, 790])
        pygame.draw.rect(window, (146, 232, 183), [
                         WINDOW_WIDTH - 395, 10, 385, 780])
        atualizaParametros = self.enterButton.exec(window)
        self.comprimentoPendulo.exec(window)
        self.amplitudePendulo.exec(window)

        self.texto1Surface = self.font.render(self.textoLinha1, True, (0, 0, 0))
        window.blit(self.texto1Surface, (830, 100))
        self.texto2Surface = self.font.render(self.textoLinha2, True, (0, 0, 0))
        window.blit(self.texto2Surface, (830, 150))

        #desenha barras de energia maxima
        pygame.draw.rect(window, (115, 115, 115), [450, 600, 200, 50])
        pygame.draw.rect(window, (115, 115, 115), [450, 670, 200, 50])

        #desenha barra de energia cinetica
        pygame.draw.rect(window, (255, 0, 0), [450, 600, self.map_range(energiacinetica, 0, energiaMax, 0, 200), 50])
        self.energiacineticaSurface = self.font.render('Energia cinética(J): ' + str(round(energiacinetica, 3)), True, (0, 0, 0))
        window.blit(self.energiacineticaSurface, (35, 610))

        #desenha barra de energia potencial
        pygame.draw.rect(window, (0, 0, 255), [450, 670, self.map_range(energiapotencial, 0, energiaMax, 0, 200), 50])
        self.energiapotencialSurface = self.font.render('Energia gravitacional (J): ' + str(round(energiapotencial, 3)), True, (0, 0, 0))
        window.blit(self.energiapotencialSurface, (35, 680))

        #desenha limite das barras
        pygame.draw.rect(window, (0, 0, 0), [445, 600, 5, 120])
        window.blit(self.zeroSurface, (440, 730))
        self.energiaMaxSurface = self.font.render(str(round(energiaMax, 3)) + ' J', True, (0, 0, 0))
        window.blit(self.energiaMaxSurface, (640, 730))

        return atualizaParametros


class Pendulo:  # x(t) = A cos(sqrt(g/L)t); x(0) = A
    def __init__(self, comprimento, anguloMax, tempoInicio):
        # pendulo comeca na posicao maxima
        self.x = POS_INICIAL[0] + comprimento * UM_METRO * math.sin(anguloMax)
        self.y = POS_INICIAL[1] + comprimento * UM_METRO * math.cos(anguloMax)

        self.raio_bola = 20
        self.comprimento = comprimento#comprimento em metros
        self.anguloMax = anguloMax
        self.angulo = anguloMax  # angulo em que o pendulo se encontra atualmente
        self.freqAngular = math.sqrt(ACELERACAO_GRAVIDADE / comprimento)

        self.energiacinetica = 0
        self.energiapotencial = 0
        self.energiaMax = 0

        self.tempoInicio = tempoInicio
        self.mass = 1#kg

    def draw(self, window):  # desenha pendulo
        pygame.draw.line(window, (0, 0, 0), POS_INICIAL, (self.x, self.y), 2)
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.raio_bola)
        pygame.draw.circle(window, (3, 252, 165),
                           (self.x, self.y), self.raio_bola - 2)

    def calcula_angulo(self):#calcula angulo do pendulo de acordo com a funcao do MHS
        return self.anguloMax * math.cos(self.freqAngular * (pygame.time.get_ticks() - self.tempoInicio) / MILISEGUNDO_PARA_SEGUNDO)

    def calcula_posicao(self):#calcula posicao do pendulo na tela
        self.angulo = self.calcula_angulo()
        self.x = POS_INICIAL[0] + self.comprimento * \
            UM_METRO * math.sin(self.angulo)
        self.y = POS_INICIAL[1] + self.comprimento * \
            UM_METRO * math.cos(self.angulo)

    def calcula_ec(self):#energia cinetica
        velocidadeAngular = -self.anguloMax * self.freqAngular * math.sin(self.freqAngular * (pygame.time.get_ticks() - self.tempoInicio) / MILISEGUNDO_PARA_SEGUNDO)

        velocidadeLinear = velocidadeAngular * self.comprimento

        return self.mass * (velocidadeLinear**2) / 2
    
    def calcula_ep(self):#energia potencial gravitacional
        return self.mass * ACELERACAO_GRAVIDADE * (self.comprimento - self.comprimento * math.cos(self.angulo))

    def exec(self, window):#desenha pendulo, chama funcoes de calcular posicao e energia
        self.calcula_posicao()
        self.freqAngular = math.sqrt(ACELERACAO_GRAVIDADE / self.comprimento)
        self.energiacinetica = self.calcula_ec()
        self.energiapotencial = self.calcula_ep()
        self.energiaMax = self.mass * ACELERACAO_GRAVIDADE * (self.comprimento - self.comprimento * math.cos(self.anguloMax))

        self.draw(window)


class Main:
    def __init__(self):

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('pendulo MHS')

        self.running = True

        self.clock = pygame.time.Clock()
        self.framerate = 60  # 60 fps.

        # parametros iniciais: 0.248 metros para ter periodo de 1 segundo, max:0.7
        self.pendulo = Pendulo(
            0.248, math.pi / 6, pygame.time.get_ticks() / MILISEGUNDO_PARA_SEGUNDO)
        self.gui = GUI()

    def run(self):#loop principal

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(self.framerate)#limita a taxa de quadros por segundo
            self.window.fill((204, 204, 204))
            self.pendulo.exec(self.window)
            atualizaParametros = self.gui.exec(self.window, self.pendulo.energiacinetica, self.pendulo.energiapotencial, self.pendulo.energiaMax)
            if atualizaParametros == CLICOU:
                self.pendulo.comprimento = self.gui.comprimentoPendulo.currentValue
                self.pendulo.anguloMax = self.gui.amplitudePendulo.currentValue
            pygame.display.update()


pygame.init()
main = Main()
main.run()
