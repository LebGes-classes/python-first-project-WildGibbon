import random

from Model.LevelGeneration.Matrix import Matrix
from Model.LevelGeneration.MatrixPathBuilder import MatrixPathBuilder


class Maze:
    """
    Класс для генерации лабиринта с использованием MatrixPathBuilder.
    """
    def __init__(self, path_builder: MatrixPathBuilder, exits_count: int):
        """
        Инициализирует генератор лабиринта.

        Args:
            path_builder: Строитель пути для создания структуры лабиринта.
            exits_count: Количество выходов, которые нужно сгенерировать.
        """
        self.__path_builder = path_builder
        self.__exits_count = exits_count
        self.__exit_coordinate = (0, 0)
        self.__generate()

    def to_matrix(self) -> Matrix:
        """
        Возвращает сгенерированный лабиринт в виде объекта Matrix.
        """
        return self.__path_builder.matrix

    @property
    def exit_coordinate(self) -> tuple[int, int]:
        """
        Возвращает координаты последнего сгенерированного выхода.
        """
        return self.__exit_coordinate

    def __generate(self) -> None:
        """
        Выполняет генерацию лабиринта, создавая пути и выходы.
        """
        exits = 0
        while len(self.__path_builder.traceback) > 0:
            if self.__path_builder.allowed_build_directions():
                self.__path_builder.build(1, random.choice(self.__path_builder.allowed_build_directions()))
            else:
                if exits < self.__exits_count and self.__path_builder.can_make_exit() and random.randint(0, exits + 1) == 0:
                    self.__path_builder.try_make_exit()
                    self.__exit_coordinate = self.__path_builder.get_cursor()
                    exits += 1
                self.__path_builder.rollback()
            print()
