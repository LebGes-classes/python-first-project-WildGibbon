import keyboard
from typing import Any


class Menu:
    """
    Класс для создания и управления интерактивным меню в консоли.
    """
    def __init__(self, list_of_items: list[str], view: Any, general_banner: str) -> None:
        """
        Инициализирует меню с заданным списком пунктов, представлением и баннером.

        Args:
            list_of_items: Список строковых элементов меню.
            view: Объект представления для отображения меню.
            general_banner: Общий баннер, отображаемый над пунктами меню.
        """
        self.__general_banner = general_banner
        self.__items = list_of_items
        self.__view = view
        self.__cursor_position = 0

    def get_selected_item(self) -> str:
        """
        Отображает меню и ожидает выбора пользователя.

        Возвращает:
            Строку с текстом выбранного пункта меню.
        """
        while True:
            self.__view.Visualize(self.__cursor_position, self.__items, self.__general_banner)
            user_input = keyboard.read_event()

            if user_input.event_type == keyboard.KEY_DOWN:
                match user_input.name:
                    case "up":
                        self.__cursor_position = max(0, self.__cursor_position - 1)

                    case "down":
                        self.__cursor_position = min(len(self.__items) - 1, self.__cursor_position + 1)

                    case "enter":
                        return self.__items[self.__cursor_position]
