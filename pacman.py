import pygame
from abc import ABCMeta, abstractmethod
import random

pygame.init()

# definiçao da tela do jogo e fontes exibidas
screen = pygame.display.set_mode((800, 600), 0)
font = pygame.font.SysFont("arial", 24, True, False)

# constantes
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
ORANGE = (255, 140, 0)
PINK = (255, 15, 192)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
SPEED = 1
UP = 1
DOWN = 2
RIGHT = 3
LEFT = 4


class GameElements(metaclass=ABCMeta):
    @abstractmethod
    def paint(self, screen):
        pass

    @abstractmethod
    def calculate_rules(self, ):
        pass

    @abstractmethod
    def process_events(self, events):
        pass


class Movable(metaclass=ABCMeta):
    @abstractmethod
    def accept_move(self):
        pass

    @abstractmethod
    def denied_move(self, direction):
        pass

    @abstractmethod
    def corner(self, direction):
        pass


class MovableValidator(metaclass=ABCMeta):
    @abstractmethod
    def add_movable(self, obj):
        pass


# classe que define cenário e recebe atores
class Scenery(GameElements):
    def __init__(self, size, pacman_scenery):
        self.pacman = pacman_scenery
        self.movables = []
        self.score = 0
        self.state = 0
        # possiveis estados: 0-jogando; 1-pausado; 3-vitoria
        self.size = size
        self.lifes = 3
        self.matrix = [
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 0, 0, 0, 0, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 2, 0, 0, 0, 0, 0, 0, 2, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 1, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2],
            [2, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 2, 2, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 1, 2, 2, 2, 2, 2, 1, 2, 2, 2, 2, 1, 2],
            [2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
            [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
        ]

    # adiciona objetos movíveis(atores) no cenário.
    def add_movable(self, obj):
        self.movables.append(obj)

    # cria o texto da pontuação
    def paint_score(self, tela):
        score_x = self.size * 30
        img_score = font.render(f'Score: {self.score}', True, YELLOW)
        img_lifes = font.render(f'Lifes: {self.lifes}', True, YELLOW)
        screen.blit(img_score, (score_x, 200))
        screen.blit(img_lifes, (score_x, 250))


    # cria as paredes do cenário
    def paint_line(self, screen, line_number, line):
        for column_number, column in enumerate(line):
            x = column_number * self.size
            y = line_number * self.size
            half = self.size // 2
            color = BLACK
            if column == 2:
                color = BLUE
            pygame.draw.rect(screen, color, (x, y, self.size, self.size), 0)
            if column == 1:
                pygame.draw.circle(screen, YELLOW, (x + half, y + half), self.size // 10, 0)

    # define os estados do jogo (jogando, pausada, game over ou vitória)
    def paint(self, screen):
        if self.state == 0:
            self.paint_playing(screen)
        elif self.state == 1:
            self.paint_playing(screen)
            self.paint_paused(screen)
        elif self.state == 2:
            self.paint_playing(screen)
            self.paint_gameover(screen)
        elif self.state == 3:
            self.paint_playing(screen)
            self.paint_win(screen)

    # cria texto do estado na tela
    def paint_text_center(self, screen, text):
        text_img = font.render(text, True, YELLOW)
        text_x = (screen.get_width() - text_img.get_width()) // 1,25
        text_y = (screen.get_height() - text_img.get_height()) // 1,25
        screen.blit(text_img, (text_x, text_y))



    # exibe estado Vitoria
    def paint_win(self, screen):
        self.paint_text_center(screen, "Y O U  W I N !")

    # exibe estado Game Over
    def paint_gameover(self, screen):
        self.paint_text_center(screen, "G A M E  O V E R")

    # exibe estado Pausado
    def paint_paused(self, screen):
        self.paint_text_center(screen, "P A U S E D")

    # exibe pontuaçao do jogo
    def paint_playing(self, screen):
        for line_number, line in enumerate(self.matrix):
            self.paint_line(screen, line_number, line)
        self.paint_score(screen)

    # define a direçao do pacman
    def get_direction(self, line, column):
        direction = []
        if self.matrix[int(line - 1)][int(column)] != 2:
            direction.append(UP)
        if self.matrix[int(line + 1)][int(column)] != 2:
            direction.append(DOWN)
        if self.matrix[int(line)][int(column - 1)] != 2:
            direction.append(LEFT)
        if self.matrix[int(line)][int(column + 1)] != 2:
            direction.append(RIGHT)
        return direction

    #define regras para estado do jogo
    def calculate_rules(self):
        if self.state == 0:
            self.calculate_rules_playing()
        elif self.state == 1:
            self.calculate_rules_paused()
        elif self.state == 2:
            self.calculate_rules_gameover()

    def calculate_rules_gameover(self):
        pass

    def calculate_rules_paused(self):
        pass
    # define regras de negocio do jogo
    def calculate_rules_playing(self):
        # invoca e define regras de movimentaçao dos objetos moviveis(atores)
        for movable in self.movables:
            lin = int(movable.line)
            col = int(movable.column)
            lin_intention = int(movable.line_intention)
            col_intention = int(movable.column_intention)
            direction = self.get_direction(lin, col)
            if len(direction) >= 3:
                movable.corner(direction)
            if isinstance(movable, Ghost) and movable.line == self.pacman.line and movable.column == self.pacman.column:
                self.lifes -= 1
                if self.lifes <= 0:
                    self.state = 2
                else:
                    self.pacman.line = 1
                    self.pacman.column = 1
            else:
                if 0 <= col_intention < 28 and 0 <= lin_intention < 29 and \
                        self.matrix[lin_intention][col_intention] != 2:
                    movable.accept_move()
                    # condicao para saber se objeto movivel é a instancia pacman, se sim, come pontinhos e pontua
                    if isinstance(movable, Pacman) and self.matrix[lin][col] == 1:
                        self.score += 1
                        self.matrix[lin][col] = 0
                        if self.score >= 310:
                            self.state = 3
                else:
                    movable.denied_move(direction)
    # processa estados do jogo e define Quit
    def process_events(self, evts):
        for e in evts:
            if e.type == pygame.QUIT:
                exit()
            # define tecla P mudar o estado do jogo para pausado
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_p:
                    if self.state == 0:
                        self.state = 1
                    else:
                        self.state = 0

# cria o Pacman
class Pacman(GameElements, Movable):
    def __init__(self, size):
        self.column = 1
        self.line = 1
        self.center_x = 400
        self.center_y = 300
        self.size = size
        self.speed_x = 0
        self.speed_y = 0
        self.radius = self.size // 2
        self.column_intention = self.column
        self.line_intention = self.line
        self.opening = 0
        self.speed_opening = 1

    # define as regras do Pacman
    def calculate_rules(self):
        self.column_intention = self.column + self.speed_x
        self.line_intention = self.line + self.speed_y
        self.center_x = int(self.column * self.size + self.radius)
        self.center_y = int(self.line * self.size + self.radius)

    # cria o desenho do Pacman e cria o movimento de sua boca
    def paint(self, screen):
        # desenha corpo do pacman
        pygame.draw.circle(screen, YELLOW, (self.center_x, self.center_y), self.radius, 0)

        self.opening += self.speed_opening
        if self.opening > self.radius:
            self.speed_opening = -1
        if self.opening <= 0:
            self.speed_opening = 1

        # desenho da boca
        mouths_corner = (self.center_x, self.center_y)
        upper_lip = (self.center_x + self.radius, self.center_y - self.opening)
        lower_lip = (self.center_x + self.radius, self.center_y + self.opening)
        mouths_points = [mouths_corner, upper_lip, lower_lip]
        pygame.draw.polygon(screen, BLACK, mouths_points, 0)

        # desenho do olho
        eye_x = int(self.center_x + self.radius / 3)
        eye_y = int(self.center_y - self.radius * 0.70)
        eye_radius = int(self.radius / 10)
        pygame.draw.circle(screen, BLACK, (eye_x, eye_y), eye_radius, 0)

    # processa a mecanica de movimentacao do pecman atraves das teclas
    def process_events(self, events):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = SPEED
                elif e.key == pygame.K_LEFT:
                    self.speed_x = - SPEED
                elif e.key == pygame.K_UP:
                    self.speed_y = - SPEED
                elif e.key == pygame.K_DOWN:
                    self.speed_y = SPEED
            elif e.type == pygame.KEYUP:
                if e.key == pygame.K_RIGHT:
                    self.speed_x = 0
                elif e.key == pygame.K_LEFT:
                    self.speed_x = 0
                elif e.key == pygame.K_UP:
                    self.speed_y = 0
                elif e.key == pygame.K_DOWN:
                    self.speed_y = 0
    # aceita movimento quando for possivel
    def accept_move(self):
        self.line = self.line_intention
        self.column = self.column_intention
    # neha o movimento quando for necessario
    def denied_move(self, direction):
        self.line_intention = self.line
        self.column_intention = self.column

    def corner(self, direction):
        pass

# cria os Fantasmas(atores) (blinky, inky, clyde e pinky)
class Ghost(GameElements):
    def __init__(self, color, size):
        self.column = 13.0
        self.line = 15.0
        self.line_intention = self.line
        self.column_intention = self.column
        self.speed = 1
        self.direction = DOWN
        self.size = size
        self.color = color
    # define o padrao para criaçao do desenho dos fantasmas
    def paint(self, scree):
        slice = self.size // 8
        px = int(self.column * self.size)
        py = int(self.line * self.size)
        contour = [(px, py + self.size),
                   (px + slice, py + slice * 2),
                   (px + slice * 2, py + slice // 2),
                   (px + slice * 3, py),
                   (px + slice * 5, py),
                   (px + slice * 6, py + slice // 2),
                   (px + slice * 7, py + slice * 2),
                   (px + self.size, py + self.size)]
        pygame.draw.polygon(screen, self.color, contour, 0)

        # define o tamanho e posiçao dos olhos dos fantasmas
        eye_radius_ext = slice
        eye_radius_int = slice // 2
        eye_left_x = int(px + slice * 2.5)
        eye_left_y = int(py + slice * 2.5)
        eye_right_x = int(px + slice * 5.5)
        eye_right_y = int(py + slice * 2.5)

        pygame.draw.circle(screen, WHITE, (eye_left_x, eye_left_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_left_x, eye_left_y), eye_radius_int, 0)
        pygame.draw.circle(screen, WHITE, (eye_right_x, eye_left_y), eye_radius_ext, 0)
        pygame.draw.circle(screen, BLACK, (eye_right_x, eye_left_y), eye_radius_int, 0)

    # define as regras dos fantasmas
    def calculate_rules(self):
        if self.direction == UP:
            self.line_intention -= self.speed
        elif self.direction == DOWN:
            self.line_intention += self.speed
        elif self.direction == LEFT:
            self.column_intention -= self.speed
        elif self.direction == RIGHT:
            self.column_intention += self.speed

    # define a regra de movimentaçao dos fantamas
    def change_direction(self, direction):
        self.direction = random.choice(direction)

    # define movimentaçao do fantasma ao chegar numa encruzilhada
    def corner(self, direction):
        self.change_direction(direction)
    # aceita o movimento se for possivel
    def accept_move(self):
        self.line = self.line_intention
        self.column = self.column_intention
    # nega o movimento se for necessario
    def denied_move(self, direction):
        self.line_intention = self.line
        self.column_intention = self.column
        self.change_direction(direction)

    def process_events(self, evts):
        pass

if __name__ == "__main__":
    size = 600 // 30
    pacman = Pacman(size)
    blinky = Ghost(RED, size)
    inky = Ghost(CYAN, size)
    clyde = Ghost(ORANGE, size)
    pinky = Ghost(PINK, size)
    scenery = Scenery(size, pacman)
    scenery.add_movable(pacman)
    scenery.add_movable(blinky)
    scenery.add_movable(inky)
    scenery.add_movable(clyde)
    scenery.add_movable(pinky)

    while True:
        # calcula regras
        pacman.calculate_rules()
        blinky.calculate_rules()
        inky.calculate_rules()
        clyde.calculate_rules()
        pinky.calculate_rules()
        scenery.calculate_rules()

        # pintar a tela
        screen.fill(BLACK)
        scenery.paint(screen)
        pacman.paint(screen)
        blinky.paint(screen)
        inky.paint(screen)
        clyde.paint(screen)
        pinky.paint(screen)
        pygame.display.update()
        pygame.time.delay(100)

        # captura de eventos
        events = pygame.event.get()
        pacman.process_events(events)
        scenery.process_events(events)
