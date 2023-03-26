import pygame
import math

UM_METRO = 1000  # 1000 pixels
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
POS_INICIAL = (400, 50)  # posicao do fio
ACELERACAO_GRAVIDADE = 9.8
MILISEGUNDO_PARA_SEGUNDO = 1000
CLICOU = 1
NAO_CLICOU = 0


class Botao:

    def __init__(self, pos, size, text, unselectedColor, selectedColor):
        super().__init__()
        self.pos = pos
        self.size = size
        self.text = text
        self.font = pygame.font.Font(None, 80)
        self.textSurface = self.font.render(text, True, (0, 0, 0))
        self.unselectedColor = unselectedColor
        self.selectedColor = selectedColor

        self.currentColor = self.unselectedColor
        self.selected = False
        self.clicked = False

    def checkHovering(self):
        mousePos = pygame.mouse.get_pos()
        if (mousePos[0] > self.pos[0] and mousePos[0] < self.pos[0] + self.size[0]) and (mousePos[1] > self.pos[1] and mousePos[1] < self.pos[1] + self.size[1]):
            return True
        return False

    def exec(self, window):
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

        # self.map_range(self.buttonPos[0], self.pos[0], self.pos[0] + self.size[0], self.min, self.max)#min
        self.currentValue = min

        self.buttonPos = [self.pos[0], self.pos[1] + 5]
        self.buttonRadius = 15

        self.textSurface = self.font.render(text, True, (0, 0, 0))

        self.min = min
        self.max = max

    def checkHovering(self):
        mousePos = pygame.mouse.get_pos()
        if math.sqrt((self.buttonPos[0] - mousePos[0])**2 + (self.buttonPos[1] - mousePos[1])**2) < self.buttonRadius:
            return True
        return False

    def map_range(self, x, in_min, in_max, out_min, out_max):
        return (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    def exec(self, window):
        if self.checkHovering():
            self.currentColor = self.selectedColor
            if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                print('fala')
                self.clicked = True
            elif pygame.mouse.get_pressed()[0] == 0:
                self.clicked = False
        elif pygame.mouse.get_pressed()[0] == 0:
            self.currentColor = self.unselectedColor
            self.clicked = False

        if self.clicked == True and pygame.mouse.get_pos()[0] > self.pos[0] and pygame.mouse.get_pos()[0] < self.pos[0] + self.size[0]:
            self.buttonPos[0] = pygame.mouse.get_pos()[0]

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
            (WINDOW_WIDTH - 400 + 50, 500), 'Amplitude (rad)', (7, 242, 70), (3, 163, 46), 0.01, math.pi / 2)

    def exec(self, window):
        pygame.draw.rect(window, (0, 0, 0), [WINDOW_WIDTH - 400, 5, 395, 790])
        pygame.draw.rect(window, (146, 232, 183), [
                         WINDOW_WIDTH - 395, 10, 385, 780])
        atualizaParametros = self.enterButton.exec(window)
        self.comprimentoPendulo.exec(window)
        self.amplitudePendulo.exec(window)

        return atualizaParametros


class Pendulo:  # x(t) = A cos(sqrt(g/L)t); x(0) = A
    def __init__(self, comprimento, anguloMax, tempoInicio):
        # pendulo comeca na posicao maxima
        self.x = POS_INICIAL[0] + comprimento * UM_METRO * math.sin(anguloMax)
        self.y = POS_INICIAL[1] + comprimento * UM_METRO * math.cos(anguloMax)
        self.raio_bola = 20
        self.comprimento = comprimento
        self.anguloMax = anguloMax
        self.angulo = anguloMax  # angulo em que o pendulo se encontra atualmente
        self.freqAngular = math.sqrt(ACELERACAO_GRAVIDADE / comprimento)

        self.tempoInicio = tempoInicio

    def draw(self, window):  # desenha pendulo
        pygame.draw.line(window, (0, 0, 0), POS_INICIAL, (self.x, self.y), 2)
        pygame.draw.circle(window, (0, 0, 0), (self.x, self.y), self.raio_bola)
        pygame.draw.circle(window, (3, 252, 165),
                           (self.x, self.y), self.raio_bola - 2)

    def calcula_angulo(self):
        return self.anguloMax * math.cos(self.freqAngular * (pygame.time.get_ticks() - self.tempoInicio) / MILISEGUNDO_PARA_SEGUNDO)

    def calcula_posicao(self):
        angulo = self.calcula_angulo()
        self.x = POS_INICIAL[0] + self.comprimento * \
            UM_METRO * math.sin(angulo)
        self.y = POS_INICIAL[1] + self.comprimento * \
            UM_METRO * math.cos(angulo)

    def exec(self, window):
        self.calcula_posicao()
        self.freqAngular = math.sqrt(ACELERACAO_GRAVIDADE / self.comprimento)
        self.draw(window)


class Main:
    def __init__(self):

        self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('pendulo MHS')

        self.running = True

        self.clock = pygame.time.Clock()
        self.framerate = 60  # 60 fps.

        # 0.248 metros para ter periodo de 1 segundo, pi/6. max:0.7 para comprimento
        self.pendulo = Pendulo(
            0.248, math.pi / 6, pygame.time.get_ticks() / MILISEGUNDO_PARA_SEGUNDO)
        self.gui = GUI()

    def run(self):

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.clock.tick(self.framerate)
            self.window.fill((204, 204, 204))
            self.pendulo.exec(self.window)
            atualizaParametros = self.gui.exec(self.window)
            if atualizaParametros == CLICOU:
                self.pendulo.comprimento = self.gui.comprimentoPendulo.currentValue
                self.pendulo.anguloMax = self.gui.amplitudePendulo.currentValue
            pygame.display.update()


pygame.init()
main = Main()
main.run()
