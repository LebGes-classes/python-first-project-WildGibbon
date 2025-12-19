import os

from Model.colors import Color


class Renderer:
    """
    Статический класс для управления выводом в консоль, включая очистку экрана и изменение цвета текста.
    """
    @staticmethod
    def render(string: str) -> None:
        """
        Выводит переданную строку в консоль.

        Args:
            string: Строка для вывода.
        """
        print(string)

    @staticmethod
    def clear() -> None:
        """
        Очищает экран консоли.
        """
        os.system("cls")

    @staticmethod
    def set_render_color(r: int, g: int, b: int) -> None:
        """
        Устанавливает цвет текста в консоли с помощью RGB.

        Args:
            r: Красный компонент (0-255).
            g: Зеленый компонент (0-255).
            b: Синий компонент (0-255).
        """
        print(f"\033[38;2;{r};{g};{b}m")

    @staticmethod
    def reset_render_color() -> None:
        """
        Сбрасывает цвет текста в консоли к значению по умолчанию.
        """
        print(Color.RESET)
