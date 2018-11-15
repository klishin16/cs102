import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width=640, height=480, cell_size=10, speed=10):
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

        # Создание списка клеток
        # PUT YOUR CODE HERE

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_grid()

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            # PUT YOUR CODE HERE

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True):
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist = []
        if randomize is True:
            row = []
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    row.append(random.randrange(0, 2))
                self.clist.append(row)
                row = []
        return self.clist

    def draw_cell_list(self, rects):
        """ Отображение списка клеток
        :param rects: Список клеток для отрисовки, представленный в виде матрицы
        """
        for row in range(len(rects)):
            for col in range(len(rects[0])):
                rect = (self.cell_size * col, self.cell_size * row, self.cell_size, self.cell_size)
                if rects[row][col] == 1:
                    pygame.draw.rect(self.screen, pygame.Color('green'), rect)
                else:
                    pygame.draw.rect(self.screen, pygame.Color('white'), rect)

    def get_neighbours(self, cell):
        """ Вернуть список соседей для указанной ячейки
        :param cell: Позиция ячейки в сетке, задается кортежем вида (row, col)
        :return: Одномерный список ячеек, смежных к ячейке cell
        """
        neighbours = []
        row, col = cell
        for columns in range(row - 1, row + 2):
            for rows in range(col - 1, col + 2):
                if (columns, rows) != cell and columns >= 0 and columns < len(self.clist) and rows >= 0 and rows < len(self.clist[0]):
                    neighbours.append(self.clist[columns][rows])
        return neighbours

    def update_cell_list(self, cell_list):
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = []
        # PUT YOUR CODE HERE
        return self.clist

if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
