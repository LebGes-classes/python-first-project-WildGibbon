from typing import Any

from Model.Input.InputEnums import MoveVectors
from Model.LevelGeneration.Matrix import Matrix
from View.MatrixCharacterView import MatrixCharacterView


class MatrixCharacter:
    """
    Представляет персонажа, который может перемещаться по матрице (лабиринту).
    """
    def __init__(self, matrix: Matrix, view: MatrixCharacterView, current_x: int, current_y: int, one_symbol: str) -> None:
        """
        Инициализирует персонажа на матрице.

        Args:
            matrix: Матрица, по которой перемещается персонаж.
            view: Представление для отображения персонажа и его движений.
            current_x: Начальная координата X персонажа.
            current_y: Начальная координата Y персонажа.
            one_symbol: Символ, обозначающий стену (непроходимую ячейку).
        """
        self.__one_symbol = one_symbol
        self.__current_x = current_x
        self.__current_y = current_y
        self.__matrix = matrix
        self.__view = view
        self.__view.visualize_move(self.__current_x, self.__current_y)

    @property
    def position(self) -> tuple[int, int]:
        """
        Возвращает текущую позицию персонажа в виде кортежа (x, y).
        """
        return self.__current_x, self.__current_y

    def try_move(self, direction: MoveVectors) -> None:
        """
        Пытается переместить персонажа в заданном направлении.
        Если движение возможно, обновляет позицию персонажа.
        В противном случае, визуализирует столкновение со стеной.

        Args:
            direction: Направление движения из перечисления MoveVectors.
        """
        next_x = direction.value[0] + self.__current_x
        next_y = direction.value[1] + self.__current_y

        if self.allowed_move(direction):
            self.__current_x = next_x
            self.__current_y = next_y
            self.__view.visualize_move(self.__current_x, self.__current_y)
        else:
            self.__view.visualize_wall(next_x, next_y)

    def allowed_move(self, direction: MoveVectors) -> bool:
        """
        Проверяет, возможно ли движение в заданном направлении.

        Args:
            direction: Направление движения из перечисления MoveVectors.

        Returns:
            True, если движение разрешено, иначе False.
        """
        next_x = direction.value[0] + self.__current_x
        next_y = direction.value[1] + self.__current_y
        matrix = self.__matrix

        return (0 <= next_x < matrix.width and 0 <= next_y < matrix.height and
                matrix.get(next_x, next_y) != self.__one_symbol)
