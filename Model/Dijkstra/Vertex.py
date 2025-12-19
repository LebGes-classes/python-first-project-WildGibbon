from typing import Any, Optional


class Vertex:
    """
    Представляет вершину в графе с координатами x и y.
    Используется в алгоритме Дейкстры для хранения информации о расстоянии и родителе.
    """
    def __init__(self, x: int, y: int) -> None:
        """
        Инициализирует вершину с заданными координатами.

        Args:
            x: Координата X вершины.
            y: Координата Y вершины.
        """
        self.__x = x
        self.__y = y
        self.__parent: Optional['Vertex'] = None
        self.distance: int = 99999999

    @property
    def x(self) -> int:
        """
        Возвращает координату X вершины.
        """
        return self.__x

    @property
    def y(self) -> int:
        """
        Возвращает координату Y вершины.
        """
        return self.__y

    @property
    def parent(self) -> Optional['Vertex']:
        """
        Возвращает родительскую вершину в пути.
        """
        return self.__parent

    def set_parent(self, parent: 'Vertex') -> None:
        """
        Устанавливает родительскую вершину.

        Args:
            parent: Родительская вершина.
        """
        self.__parent = parent
