"""
Модуль генерации пути в матрице уровня.

Содержит класс MatrixPathBuilder, который управляет построением траектории
по матрице, контролирует курсор, проверяет допустимость шагов и,
при необходимости, создает выход у границ уровня.
"""

import random
from typing import Any

from Model.Input.InputEnums import MoveVectors
from Model.LevelGeneration.Matrix import Matrix


class MatrixPathBuilder:
    """
    Класс для пошагового построения пути в матрице уровня.

    Управляет положением курсора, отмечает пройденные клетки, хранит путь
    (traceback) и позволяет создавать выход у границы, е��ли это возможно.
    """

    def __init__(self, cursor_x: object, cursor_y: object, matrix: Matrix) -> None:
        """
        Инициализирует построитель пути и подготавливает матрицу.

        Args:
            cursor_x: Начальная позиция курсора по оси X.
            cursor_y: Начальная позиция курсора по оси Y.
            matrix: Экземпляр матрицы, в которой строится путь.
        """
        self.__matrix = matrix
        self.__height = matrix.height
        self.__width = matrix.width
        self.__cursor_x = cursor_x
        self.__cursor_y = cursor_y
        self.__passed_points = set()
        self.__border_points = set()
        self.__traceback = []
        matrix.set_zero(cursor_x, cursor_y)
        self.__update_traceback()
        for p in [(x, y) for x in range(self.__width) for y in range(self.__height)
                  if x == 0 or x == self.__width - 1 or y == self.__height - 1 or y == 0]:
            self.__border_points.add(p)

    @property
    def traceback(self) -> list[Any]:
        """
        Возвращает накопленный путь перемещения курсора.

        Returns:
            Список кортежей координат (x, y), отражающих последовательность
            пройденных точек, включая текущую позицию.
        """
        return self.__traceback

    @property
    def matrix(self) -> Matrix:
        """
        Возвращает матрицу, в которой строится путь.

        Returns:
            Экземпляр Matrix, используемый для построения пути.
        """
        return self.__matrix

    def build(self, distance: object, direction: object) -> None:
        """
        Выполняет построение пути на заданное число шагов в направлении.

        На каждом шаге проверяет допустимость перемещения; если шаг допустим,
        перемещает курсор, отмечает клетку как посещённую и обновляет traceback.
        По завершении печатает матрицу.

        Args:
            distance: Количество шагов, которое нужно сделать.
            direction: Направление перемещения (элемент MoveVectors).
        """
        for i in range(distance):
            if self.is_allowed_build(direction):
                self.__cursor_x += direction.value[0]
                self.__cursor_y += direction.value[1]
                self.__matrix.set_zero(self.__cursor_x, self.__cursor_y)
                self.__passed_points.add((self.__cursor_x, self.__cursor_y))

            self.__update_traceback()
        self.__matrix.print_matrix()

    def set_cursor(self, x: object, y: object) -> None:
        """
        Устанавливает курсор в указанные координаты без проверки допустимости.

        Args:
            x: Координата по оси X.
            y: Координата по оси Y.
        """
        self.__cursor_x = x
        self.__cursor_y = y

    def rollback(self) -> None:
        """
        Откатывает состояние курсора на предыдущую точку пути.

        Удаляет последний элемент из traceback и устанавливает курсор на
        предыдущую позицию, если таковая существует.
        """
        self.__traceback = self.__traceback[:-1]
        if self.__traceback:
            self.set_cursor(*self.__traceback[-1])

    def is_allowed_build(self, direction: MoveVectors) -> bool:
        """
        Проверяет, допустим ли следующий шаг в указанном направлении.

        Условие допустимости:
        - следующая клетка находится внутри внутренних границ матрицы (не край);
        - клетка ранее не посещалась;
        - среди соседей следующей клетки нет уже посещённых клеток
          (кроме текущей позиции курсора).

        Args:
            direction: Направление перемещения (элемент MoveVectors).

        Returns:
            True, если шаг допустим, иначе False.
        """
        next_x = self.__cursor_x + direction.value[0]
        next_y = self.__cursor_y + direction.value[1]

        return ((0 < next_x < self.__width - 1) and (0 < next_y < self.__height - 1) and
                (next_x, next_y) not in self.__passed_points and
                all(point == (self.__cursor_x, self.__cursor_y) or point not in self.__passed_points
                    for point in self.__neighbour_points((next_x, next_y))))

    def allowed_build_directions(self) -> list[int]:
        """
        Возвращает список направлений, в которые можно сделать следующий шаг.

        Returns:
            Список элементов MoveVectors, соответствующих допустимым направлениям.
        """
        return [i for i in [MoveVectors.UP,
                            MoveVectors.RIGHT,
                            MoveVectors.LEFT,
                            MoveVectors.DOWN] if self.is_allowed_build(i)]

    def get_cursor(self) -> tuple[Any, Any]:
        """
        Возвращает текущие координаты курсора.

        Returns:
            Кортеж (x, y) текущего положения курсора.
        """
        return self.__cursor_x, self.__cursor_y

    def print_matrix(self) -> None:
        """
        Печатает текущее состояние матрицы с помощью рендерера.
        """
        self.__matrix.print_matrix()

    def try_make_exit(self) -> None:
        """
        Пытается создать выход у границы, если соседняя клетка является границей.

        Если у текущей позиции курсора есть соседи, принадлежащие множеству
        граничных точек, случайным образом выбирается один из таких соседей и
        отмечается как проходимый (нуль-символом в матрице).
        """
        neighbours = self.__neighbour_points((self.__cursor_x, self.__cursor_y))
        border_neighbours = [point for point in neighbours if point in self.__border_points]
        if border_neighbours:
            self.__matrix.set_zero(*random.choice(border_neighbours))

    def can_make_exit(self) -> bool:
        """
        Проверяет возможность создания выхода у границы из текущей позиции.

        Returns:
            True, если среди соседей текущей позиции есть граничные точки, иначе False.
        """
        neighbours = self.__neighbour_points((self.__cursor_x, self.__cursor_y))
        border_neighbours = [point for point in neighbours if point in self.__border_points]
        return len(border_neighbours) > 0

    def __update_traceback(self) -> None:
        """
        Добавляет текущую позицию курсора в историю пути (traceback).
        """
        self.__traceback.append((self.__cursor_x, self.__cursor_y))

    @staticmethod
    def __neighbour_points(point: object) -> list:
        """
        Возвращает список соседних по четырём направлениям точек для указанной.

        Args:
            point: Кортеж координат (x, y) исходной точки.

        Returns:
            Список кортежей координат соседних точек: вверх, вправо, вниз, влево.
        """
        points = [(point[0], point[1] - 1),
                  (point[0] + 1, point[1]),
                  (point[0], point[1] + 1),
                  (point[0] - 1, point[1])]

        return points
