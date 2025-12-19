from Model.Render.Renderer import Renderer


class MenuView:
    """
    Класс для визуализации меню в консоли.
    """
    def Visualize(self, cursor_position: int, items: list[str], general_banner: str) -> None:
        """
        Отображает меню с курсором на выбранном пункте.

        Args:
            cursor_position: Индекс текущего выбранного пункта меню.
            items: Список всех пунктов меню.
            general_banner: Баннер, отображаемый над меню.
        """
        Renderer.clear()
        Renderer.render(general_banner)

        for i in range(len(items)):
            if i == cursor_position:
                Renderer.render(f">{items[i]}")
            else:
                Renderer.render(f" {items[i]}")
