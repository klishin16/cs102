import pygame
from pygame.locals import *
import random


class GameOfLife:

    def __init__(self, width: int=640, height: int=480, cell_size: int=10, speed: int=10) -> None:
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

    def draw_grid(self) -> None:
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
        self.cell_list(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False

            self.draw_cell_list(self.clist)
            self.draw_grid()
            self.update_cell_list(self.clist)

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def cell_list(self, randomize=True) -> list:
        """ Создание списка клеток.
        :param randomize: Если True, то создается список клеток, где
        каждая клетка равновероятно может быть живой (1) или мертвой (0).
        :return: Список клеток, представленный в виде матрицы
        """
        self.clist: list = []
        if randomize is True:
            row = []
            for i in range(self.cell_height):
                for j in range(self.cell_width):
                    row.append(random.randrange(0, 2))
                self.clist.append(row)
                row = []
        return self.clist

    def draw_cell_list(self, rects: list) -> None:
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

    def get_neighbours(self, cell: tuple) -> list:
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

    def update_cell_list(self, cell_list: list) -> list:
        """ Выполнить один шаг игры.
        Обновление всех ячеек происходит одновременно. Функция возвращает
        новое игровое поле.
        :param cell_list: Игровое поле, представленное в виде матрицы
        :return: Обновленное игровое поле
        """
        new_clist = []

        for row in range(len(cell_list)):
            line = []
            for col in range(len(cell_list[0])):
                neighbours = self.get_neighbours((row, col))
                number_of_neighbours = 0
                for neighbour in neighbours:
                    if neighbour == 1:
                        number_of_neighbours += 1
                if (cell_list[row][col] == 1 and number_of_neighbours >= 2 and number_of_neighbours <= 3) or (cell_list[row][col] == 0 and number_of_neighbours == 3):
                    line.append(1)
                else:
                    line.append(0)
            new_clist.append(line)
        self.clist = new_clist
        return self.clist


if __name__ == '__main__':
    game = GameOfLife(320, 240, 20)
    game.run()
