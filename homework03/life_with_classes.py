import pygame
from pygame.locals import *
import random
from copy import deepcopy


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=40, speed=10):
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_grid(self):
        """ Отрисовать сетку """
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.width, y))

    def run(self):
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')
        self.screen.fill(pygame.Color('white'))

        self.cellList = CellList(self.cell_height, self.cell_width, randomize=True)
        #self.cellList = CellList.from_file("game.txt")

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_cell_list(self.cellList)
            self.draw_grid()
            self.cellList.update()
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def draw_cell_list(self, cellList):
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for cell in cellList:
            rect = (self.cell_size * cell.col, self.cell_size * cell.row, self.cell_size, self.cell_size)
            if cell.state == 1:
                pygame.draw.rect(self.screen, pygame.Color('green'), rect)
            else:
                pygame.draw.rect(self.screen, pygame.Color('white'), rect)


class Cell:

    def __init__(self, row, col, state=False):
        self.row = row
        self.col = col
        self.state = state

    def is_alive(self):
        return self.state


class CellList:

    def __init__(self, nrows, ncols, randomize=False):
        self.nrows = nrows
        self.ncols = ncols
        self.randomize = randomize

        fillList = []
        for rows in range(nrows):
            for cols in range(ncols):
                if (self.randomize is True):
                    fillList.append(Cell(rows, cols, random.randrange(0, 2)))
                else:
                    fillList.append(Cell(rows, cols))

        self.clist = fillList

    def get_neighbours(self, myCell) -> list:
        neighbours = []
        row, col = myCell
        for cell in self:
            if abs(row - cell.row) <= 1 and abs(col - cell.col) <= 1 and abs(row - cell.row) + abs(col - cell.col) != 0:
                neighbours.append(cell.state)
        return neighbours

    def update(self):
        new_clist = deepcopy(self)
        index = 0
        for cell in new_clist:
            neighbours = self.get_neighbours((cell.row, cell.col))
            number_of_neighbours = 0
            for neighbour in neighbours:
                if neighbour == 1:
                    number_of_neighbours += 1
            if (cell.state == 1 and number_of_neighbours >= 2 and number_of_neighbours <= 3) or (cell.state == 0 and number_of_neighbours == 3):
                self.clist[index].state = 1
            else:
                self.clist[index].state = 0
            index += 1
        return self.clist

    def __iter__(self):
        self.index = 0
        return self

    def __next__(self):
        if self.index == len(self.clist):
            raise StopIteration
        cell = self.clist[self.index]
        self.index = self.index + 1
        return cell

    def __str__(self) -> str:
        out = [int(cell.state) for cell in self.clist]
        return str(out)

    @classmethod
    def from_file(self, filename):
        file = open(filename, 'r')
        data = file.read().split()
        grid = []
        for row in data:
            grid.extend([int(cell) for cell in row])
        return grid


if __name__ == '__main__':
    game = GameOfLife(480, 480, 40, speed=10)
    game.run()
