import random
import pygame
from consts import shapes

pygame.init()
pygame.font.init()


class Tetramino(object):
    def __init__(self):
        self.x = 5
        self.y = 0
        self.shape = random.choice(shapes)
        self.color = 'WHITE'
        self.rotation = 0
        self.passedTiles = 0

    def ret(self):
        self.positions = []
        shape_format = self.shape[
            self.rotation % len(self.shape)]

        for i, line in enumerate(shape_format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    self.positions.append((self.x + j, self.y + i))

        for i, pos in enumerate(self.positions):
            self.positions[i] = [pos[0] - 2, pos[1] - 4]
        for i in range(4):
            self.positions[i][1] += self.passedTiles
        return self.positions


class Grid:
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(20)]
        self.score = 0

    def showGrid(self):
        for line in self.grid:
            print(line)

    def clearFullRows(self):
        done = False
        while not done:
            for i in range(19, 0, -1):
                while self.grid[i] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                    self.score += 10
                    for j in range(i, 0, - 1):
                        self.grid[j] = self.grid[j - 1]
                        self.grid[j - 1] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
            done = True

    def retColors(self):
        colors = []
        for i in range(20):
            for j in range(10):
                if self.grid[i][j] == 1:
                    colors.append('WHITE')
                else:
                    colors.append('BLACK')
        return colors[::-1]

    def addTetramino(self, tetramino):
        for cube in tetramino:
            if cube[1] >= 0:
                try:
                    self.grid[cube[1]][cube[0]] = 1
                except:
                    pass

    def removeTetramino(self, tetramino):
        for cube in tetramino:
            if cube[1] >= 0:
                try:
                    self.grid[cube[1]][cube[0]] = 0
                except:
                    pass


def checkBottom(positions, grid):
    for pos in positions:
        if pos[1] >= 19:
            return False
    for pos in positions:
        if grid[pos[1] + 1][pos[0]] == 1 and [pos[0], pos[1] + 1] not in positions:
            if pos[1] == 0:
                gameOver()
            return False
    return True


def canMoveLeft(positions, grid):
    for pos in positions:
        if pos[0] - 1 > 9 or pos[0] - 1 < 0:
            return False
    for pos in positions:
        if grid[pos[1]][pos[0] - 1] == 1 and [pos[0] - 1, pos[1]] not in positions:
            return False
    return True


def canMoveRight(positions, grid):
    for pos in positions:
        if pos[0] + 1 > 9 or pos[0] + 1 < 0:
            return False
    for pos in positions:
        if grid[pos[1]][pos[0] + 1] == 1 and [pos[0] + 1, pos[1]] not in positions:
            return False
    return True


def drawNextTetramino(surface, tetramino):
    for pos in tetramino:
        pygame.draw.rect(surface, 'WHITE', ((30 * pos[0]) + 500, (30 * pos[1]) + 460, 29, 29))


def drawCubes(surface, desk):
    a = desk.retColors()
    for i in range(20):
        for j in range(10):
            color = a.pop()
            pygame.draw.rect(surface, color, ((30 * j) + 250, (30 * i) + 100, 30, 30))


def drawGrid(surface):
    for i in range(20):
        pygame.draw.line(surface, 'BLACK', (250, 100 + i * 30),
                         (250 + 300, 100 + i * 30))
        for j in range(10):
            pygame.draw.line(surface, 'BLACK', (250 + j * 30, 100),
                             (250 + j * 30, 100 + 600))


def drawText(surface, score):
    font = pygame.font.Font('arcade.ttf', 100, bold=True)
    label = font.render('TETRIS', 10, (255, 255, 255))

    surface.blit(label, ((250 + 300 / 2) - (label.get_width() / 2), 10))

    font = pygame.font.Font('arcade.ttf', 30)

    label_score = font.render('SCORE          ' + str(score), 1, (255, 255, 255))
    label_next = font.render('NEXT FIGURE', 1, (255, 255, 255))
    start_x_hi = 250 - 240
    start_y_hi = 100 + 200
    surface.blit(label_next, (start_x_hi + 560, start_y_hi + 200))
    surface.blit(label_score, (start_x_hi + 10, start_y_hi + 200))


def drawWindow(surface, desk, score=0):
    surface.fill('BLACK')
    drawCubes(surface, desk)
    drawText(surface, score)
    drawGrid(surface)
    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (250, 100, 300, 600), 4)


def game(window):
    desk = Grid()
    Tetraminos = []
    Tetraminos.append(Tetramino())
    Tetraminos.append(Tetramino())
    clock = pygame.time.Clock()
    newPieceRequired = True
    run = True
    delay = 150

    drawWindow(window, desk, desk.score)

    while run:
        if newPieceRequired:
            newPieceRequired = False
            nextTetr = Tetraminos[1]
            currTetr = Tetraminos[0]
            Tetraminos.append(Tetramino())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    if canMoveLeft(currTetr.ret(), desk.grid):
                        currTetr.x -= 1

                elif event.key == pygame.K_RIGHT:
                    if canMoveRight(currTetr.ret(), desk.grid):
                        currTetr.x += 1

                elif event.key == pygame.K_DOWN:  # Issue
                    if currTetr.ret()[0][1] < 16:
                        currTetr.y += 1

                elif event.key == pygame.K_UP:  # Issue
                    currTetr.rotation += 1

        currTetr.passedTiles += 1
        desk.addTetramino(currTetr.ret())
        drawWindow(window, desk, desk.score)
        drawNextTetramino(window, nextTetr.ret())
        pygame.display.flip()
        if not checkBottom(currTetr.ret(), desk.grid):
            newPieceRequired = True
            Tetraminos.pop(0)
            desk.clearFullRows()
        else:
            desk.removeTetramino(currTetr.ret())
        pygame.time.delay(delay - desk.score)
        clock.tick()


def gameOver():
    pygame.display.quit()
    quit()


def main_menu(window):
    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                game(window)
    pygame.quit()


if __name__ == '__main__':
    window = pygame.display.set_mode((800, 750), pygame.DOUBLEBUF|pygame.HWSURFACE)

    pygame.display.set_caption('Tetris')
    font = pygame.font.Font('arcade.ttf', 50, bold=True)
    label = font.render('PRESS ANY KEY TO BEGIN', 10, (255, 255, 255))
    window.blit(label, (150, 300))
    pygame.display.flip()

    main_menu(window)
