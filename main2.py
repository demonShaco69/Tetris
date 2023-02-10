import random
import pygame
from consts import shapes


class Tetramino(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = 'WHITE'
        self.rotation = 0

    def showInfo(self):
        return self.x, self.y, self.shape, self.color, self.rotation


class Grid:
    def __init__(self):
        self.grid = [[0 for x in range(10)] for y in range(20)]

    def showGrid(self):
        for line in self.grid:
            print(line)

    def clearFullRows(self):
        for i in range(len(self.grid)):
            if self.grid[i] == [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]:
                self.grid[i] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
                for j in range(i, 0, -1):
                    self.grid[j] = self.grid[j - 1]


def convertShapeFormat(tetramino):
    positions = []
    shape_format = tetramino.shape[
        tetramino.rotation % len(tetramino.shape)]

    for i, line in enumerate(shape_format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                positions.append((tetramino.x + j, tetramino.y + i))

    for i, pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    print(positions)
    return positions


def isInGrid(positions):
    for pos in positions:
        if pos[0] > 10 or pos[0] < 1:
            return False
        if pos[1] > 20 or pos[1] < 1:
            return False
    return True


def randShape():
    return Tetramino(5, 0, random.choice(shapes))


def drawGrid(surface):
    for i in range(10):
        pygame.draw.line(surface, 'BLACK', (250, 100 + i * 30),
                         (250 + 300, 100 + i * 30))
        for j in range(20):
            pygame.draw.line(surface, 'BLACK', (250 + j * 30, 100),
                             (250 + j * 30, 100 + 600))


def drawWindow(surface, desk, score=0):
    surface.fill('BLACK')

    pygame.font.init()
    font = pygame.font.Font('arcade.ttf', 65, bold=True)
    label = font.render('TETRIS', 1, (255, 255, 255))

    surface.blit(label, ((250 + 300 / 2) - (label.get_width() / 2), 30))

    font = pygame.font.Font('arcade.ttf', 30)

    label_hi = font.render('SCORE   ' + str(score), 1, (255, 255, 255))

    start_x_hi = 250 - 240
    start_y_hi = 100 + 200

    surface.blit(label_hi, (start_x_hi + 20, start_y_hi + 200))

    for i in range(10):
        for j in range(20):
            pygame.draw.rect(surface, desk[i][j],
                             (250 + j * 30, 100 + i * 30, 30, 30), 0)

    drawGrid(surface)

    border_color = (255, 255, 255)
    pygame.draw.rect(surface, border_color, (250, 100, 300, 600), 4)


def game(window):
    run = True
    desk = Grid()
    currTetramino = randShape()
    nextTetramino = randShape()
    clock = pygame.time.Clock()
    score = 0
    fallSpeed = 0.1


    while run:
        clock.tick()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    currTetramino.x -= 1  # move x position left
                    if not isInGrid(convertShapeFormat(currTetramino)):
                        currTetramino.x += 1

                elif event.key == pygame.K_RIGHT:
                    currTetramino.x += 1  # move x position right
                    if not isInGrid(convertShapeFormat(currTetramino)):
                        currTetramino.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    currTetramino.y += 1
                    if not isInGrid(convertShapeFormat(currTetramino)):
                        currTetramino.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    currTetramino.rotation = currTetramino.rotation + 1 % len(currTetramino.shape)
                    if not isInGrid(convertShapeFormat(currTetramino)):
                        currTetramino.rotation = currTetramino.rotation - 1 % len(currTetramino.shape)
        tetraminoPos = convertShapeFormat(currTetramino)


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
    win = pygame.display.set_mode((800, 750))
    pygame.display.set_caption('Tetris')

    main_menu(win)
'''def test():
    desk = Grid()
    desk.grid[15] = [1, 1, 1, 1, 0, 1, 1, 1, 1, 1]
    desk.grid[16] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    desk.grid[17] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    desk.grid[18] = [1, 1, 1, 1, 1, 1, 1, 0, 1, 1]
    desk.grid[19] = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    desk.clearFullRows()

    print('||||||||||||||||||||||||||||||')
    desk.showGrid()

test()'''
