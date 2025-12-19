from typing import Any

from Model.Render.Renderer import Renderer


class Matrix:
    """
    Класс матрицы символов с фиксированной шириной и высотой.

    Матрица хранится как список столбцов (по оси X), каждый из которых содержит
    список символов по оси Y. Предоставляет методы для чтения, записи и печати,
    а также поиска координаты первого вхождения символа.
    """

    def __init__(self, width: object, height: object, fill_symbol: object, zero_symbol) -> None:
        """
        Инициализирует матрицу заданного размера и символов.

        Args:
            width: Ширина матрицы (количество столбцов по оси X).
            height: Высота матрицы (количество строк по оси Y).
            fill_symbol: Символ, которым заполняются все ячейки по умолчанию.
            zero_symbol: Символ, используемый для обозначения «пустой/проходимой» ячейки.
        """
        self.__matrix = [[fill_symbol for y in range(height)] for x in range(width)]
        self.__zero_symbol = zero_symbol

    @property
    def height(self) -> int:
        """
        Возвращает высоту матрицы (количество строк по оси Y).

        Returns:
            Целое число — высота матрицы.
        """
        return len(self.__matrix[0])

    @property
    def width(self) -> int:
        """
        Возвращает ширину матрицы (количество столбцов по оси X).

        Returns:
            Целое число — ширина матрицы.
        """
        return len(self.__matrix)

    def get(self, x: object, y: object) -> list[Any] | list[list[Any]]:
        """
        Возвращает значение ячейки по координатам (x, y).

        Args:
            x: Координата по оси X (столбец).
            y: Координата по оси Y (строка).

        Returns:
            Значение, содержащееся в ячейке матрицы по указанным координатам.
        """
        return self.__matrix[x][y]

    def get_symbol_coord(self, symbol: object) -> tuple[int, int]:
        """
        Возвращает координаты первого вхождения символа в матрице.

        Args:
            symbol: Искомый символ.

        Returns:
            Кортеж (x, y) координат первого найденного вхождения символа.
            Если символ не найден, возвращает (0, 0).
        """
        i = [(x, y) for x in range(self.width) for y in range(self.height) if self.__matrix[x][y] == symbol]
        if i:
            return i[0]
        else:
            return 0, 0

    def exist_symbol(self, symbol: object) -> bool:
        """
        Проверяет наличие символа в матрице.

        Args:
            symbol: Искомый символ.

        Returns:
            True, если символ найден в матрице, иначе False.
        """
        return any(char == symbol for raw in self.__matrix for char in raw)

    def set_zero(self, x: object, y: object) -> None:
        """
        Устанавливает в ячейку (x, y) нулевой символ (проходимость).

        Args:
            x: Координата по оси X (столбец).
            y: Координата по оси Y (строка).
        """
        self.__matrix[x][y] = self.__zero_symbol

    def set_symbol(self, x: object, y: object, symbol: object) -> None:
        """
        Записывает указанный символ в ячейку (x, y).

        Args:
            x: Координата по оси X (столбец).
            y: Координата по оси Y (строка).
            symbol: Символ для записи в ячейку.
        """
        self.__matrix[x][y] = symbol

    def print_matrix(self) -> None:
        """
        Печатает матрицу построчно, используя рендерер.

        Каждая строка формируется транспонированием данных (по Y), после чего
        передаётся в Renderer.render для вывода.
        """
        for raw in zip(*self.__matrix):
            Renderer.render("".join(raw))

    def to_string(self):
        """
        Возвращает строковое представление матрицы.

        Returns:
            Строка, содержащая построчное представление матрицы с переводами строк.
        """
        result = ""

        for raw in zip(*self.__matrix):
            result = result + "".join(raw) + "\n"

        return result
