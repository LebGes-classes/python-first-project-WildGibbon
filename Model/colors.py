class Color:
    """
    Класс, содержащий статические методы и константы для работы с цветом в консоли
    с использованием ANSI-кодов.
    """
    RESET = "\033[0m"
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"

    @staticmethod
    def color_str_to_rgb(string: str, r: int, g: int, b: int) -> str:
        """
        Окрашивает текст в заданный RGB цвет.

        Args:
            string: Строка для окрашивания.
            r: Красный компонент (0-255).
            g: Зеленый компонент (0-255).
            b: Синий компонент (0-255).

        Returns:
            Строка с ANSI-кодами для цвета текста.
        """
        return f"\033[38;2;{r};{g};{b}m{string}" + Color.RESET

    @staticmethod
    def color_str_back_to_rgb(string: str, r: int, g: int, b: int) -> str:
        """
        Окрашивает фон текста в заданный RGB цвет.

        Args:
            string: Строка для окрашивания.
            r: Красный компонент (0-255).
            g: Зеленый компонент (0-255).
            b: Синий компонент (0-255).

        Returns:
            Строка с ANSI-кодами для цвета фона.
        """
        return f"\033[48;2;{r};{g};{b}m{string}" + Color.RESET
