from Model.LevelGeneration.Matrix import Matrix
from Model.Render.Renderer import Renderer


class MatrixCharacterView:
    """
    Класс для визуализации персонажа и его окружения на матрице.
    Создает "туман войны", скрывая неисследованные области.
    """
    def __init__(self, matrix: Matrix, unknown_symbol: str, zero_symbol: str, character_symbol: str) -> None:
        """
        Инициализирует представление персонажа.

        Args:
            matrix: Основная матрица лабиринта.
            unknown_symbol: Символ для неисследованных областей.
            zero_symbol: Символ для пустых (исследованных) областей.
            character_symbol: Символ для обозначения персонажа.
        """
        self.__view_matrix = Matrix(matrix.width, matrix.height, unknown_symbol, zero_symbol)
        self.__character_symbol = character_symbol
        self.__zero_symbol = zero_symbol
        self.__matrix = matrix

    def visualize_move(self, x: int, y: int) -> None:
        """
        Обновляет и отображает перемещение персонажа.
        Старая позиция заменяется на 'zero_symbol', новая - на 'character_symbol'.

        Args:
            x: Новая координата X персонажа.
            y: Новая координата Y персонажа.
        """
        if self.__view_matrix.exist_symbol(self.__character_symbol):
            coords = self.__view_matrix.get_symbol_coord(self.__character_symbol)
            if coords:
                self.__view_matrix.set_symbol(coords[0], coords[1], self.__zero_symbol)

        self.__view_matrix.set_symbol(x, y, self.__character_symbol)
        Renderer.clear()
        self.__view_matrix.print_matrix()

    def visualize_wall(self, x: int, y: int) -> None:
        """
        "Открывает" стену на карте вида, когда персонаж пытается в нее врезаться.

        Args:
            x: Координата X стены.
            y: Координата Y стены.
        """
        view = self.__view_matrix
        x = min(max(0, x), view.width - 1)
        y = min(max(0, y), view.height - 1)
        view.set_symbol(x, y, self.__matrix.get(x, y))
        Renderer.clear()
        self.__view_matrix.print_matrix()
