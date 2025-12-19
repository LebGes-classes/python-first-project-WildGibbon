from typing import Any, Tuple

from Model.Dijkstra.Vertex import Vertex
from Model.LevelGeneration.Matrix import Matrix


class MatrixGraph:
    """
    Представляет граф, построенный на основе матрицы, где проходимые ячейки
    являются вершинами графа.
    """
    def __init__(self, matrix: Matrix, maze_zero_char: Any):
        """
        Инициализирует граф на основе матрицы.

        Args:
            matrix: Матрица уровня.
            maze_zero_char: Символ, обозначающий проходимую ячейку.
        """
        self.__maze_zero_char = maze_zero_char
        self.__vertex_neighbours = {}
        self.__matrix = matrix
        self.__generate()

    def get_neighbours(self) -> dict[Vertex, list[Vertex]]:
        """
        Возвращает словарь, где ключи - это вершины, а значения - списки их соседей.
        """
        return self.__vertex_neighbours

    def get_vertex(self, x: int, y: int) -> Vertex | None:
        """
        Находит и возвращает вершину по её координатам.

        Args:
            x: Координата X.
            y: Координата Y.

        Returns:
            Объект Vertex или None, если вершина не найдена.
        """
        for vertex in self.__vertex_neighbours.keys():
            if vertex.x == x and vertex.y == y:
                return vertex
        return None

    def __generate(self) -> None:
        """
        Генерирует граф, создавая вершины для всех проходимых ячеек
        и устанавливая связи между соседними вершинами.
        """
        matrix = self.__matrix

        for x in range(matrix.width):
            for y in range(matrix.height):
                if matrix.get(x, y) == self.__maze_zero_char:
                    self.__vertex_neighbours[Vertex(x, y)] = []

        for x in range(matrix.width):
            for y in range(matrix.height):
                if matrix.get(x, y) == self.__maze_zero_char:
                    vertex = self.get_vertex(x, y)
                    if vertex:
                        self.__vertex_neighbours[vertex] = self.__neighbours((x, y))

    def __neighbours(self, point: Tuple[int, int]) -> list[Vertex]:
        """
        Находит всех проходимых соседей для данной точки (вершины).

        Args:
            point: Кортеж с координатами (x, y).

        Returns:
            Список соседних вершин.
        """
        matrix = self.__matrix
        points = [(point[0], point[1] - 1),
                  (point[0] + 1, point[1]),
                  (point[0], point[1] + 1),
                  (point[0] - 1, point[1])]
        points = [p for p in points if 0 <= p[0] < matrix.width and 0 <= p[1] < matrix.height]

        return [self.get_vertex(*p) for p in points if self.get_vertex(*p) and matrix.get(*p) == self.__maze_zero_char]
