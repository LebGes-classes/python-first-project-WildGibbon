"""
Этот модуль определяет привязки клавиш для управления движением и меню в игре.
"""
import keyboard

from Model.Input.InputEnums import *

MOVE_BINDS = {
    "up": MoveVectors.UP,
    "left": MoveVectors.LEFT,
    "down": MoveVectors.DOWN,
    "right": MoveVectors.RIGHT,
}
"""
Словарь, сопоставляющий имена клавиш управления курсором с векторами движения.
"""

MENU_BINDS = {
    "e": MenuInput.EXIT,
    "r": MenuInput.RESET
}
"""
Словарь, сопоставляющий клавиши с действиями в меню.
"""
