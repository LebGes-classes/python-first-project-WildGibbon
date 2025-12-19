from enum import Enum


class MoveVectors(Enum):
    """
    Перечисление, определяющее векторы движения для персонажа.
    Каждый элемент представляет собой кортеж (dx, dy).
    """
    UP = (0, -1)
    DOWN = (0, 1)
    LEFT = (-1, 0)
    RIGHT = (1, 0)


class MenuInput(Enum):
    """
    Перечисление, определяющее возможные действия в меню.
    """
    EXIT = 0
    RESET = 1
