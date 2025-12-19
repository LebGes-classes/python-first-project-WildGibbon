import keyboard
import random
import sys

from Model.LevelGeneration.MatrixPathBuilder import MatrixPathBuilder
from Model.Character.MatrixCharacter import MatrixCharacter
from Model.Menu.Menu import Menu
from Model.Render.Renderer import Renderer
from View.MatrixCharacterView import MatrixCharacterView
from Model.Dijkstra.MatrixGraph import MatrixGraph
from Model.LevelGeneration.Matrix import Matrix
from Model.Dijkstra.Dijkstra import Dijkstra
from Model.Input.KeyBinds import MOVE_BINDS
from Model.LevelGeneration.Maze import Maze
from View.MenuView import MenuView
from Model.colors import Color


class Game:
    """
    Основной класс игры, управляющий игровым процессом, меню и уровнями.
    """
    def __init__(self) -> None:
        """
        Инициализирует игру, устанавливая начальные значения для размеров лабиринта,
        сложности и других игровых параметров.
        """
        self.HARD_LEVEL_SIZE_INCREASE = 5
        self.EASY_LEVEL_SIZE_INCREASE = 3
        self.MAZE_ONE = Color.color_str_back_to_rgb("  ", 46, 222, 16)
        self.MAZE_CHARACTER = Color.color_str_back_to_rgb("🙂 ", 21, 54, 17)
        self.MAZE_ZERO = Color.color_str_back_to_rgb("  ", 21, 54, 17)
        self.MAZE_UNKNOWN = Color.color_str_back_to_rgb("  ", 20, 20, 20)

        self.__level_size_increase = 3
        self.__easy_mode = False
        self.__maze_height = 8
        self.__maze_width = 8
        self.__current_window = self.__main_menu

    def play(self) -> None:
        """
        Запускает основной игровой цикл, который продолжается до выхода из игры.
        """
        while True:
            self.__current_window()

    def __main_menu(self) -> None:
        """
        Отображает главное меню и обрабатывает выбор пользователя.
        """
        items = ["Играть",
                 "Выбор сложности",
                 "Выйти"]
        game_name = Color.color_str_to_rgb("⛏ МАЙНКРАФТ КРИПЕР ЛАБИРИНТ ⛏", 40, 214, 34)
        banner = (f"╔══════════════════════════════════════════════════════════════════════════╗\n"
                  f"║                      {game_name}                       ║\n"
                  f"╚══════════════════════════════════════════════════════════════════════════╝\n")

        main_menu = Menu(items, MenuView(), banner)

        match main_menu.get_selected_item():
            case "Играть":
                self.__current_window = self.__start_game_cycle
            case "Выйти":
                sys.exit()
            case "Выбор сложности":
                self.__current_window = self.__difficulty_settings

    def __win(self) -> None:
        """
        Отображает экран победы после прохождения уровня, показывая статистику
        и предлагая варианты для продолжения.
        """
        graph = MatrixGraph(self.maze.to_matrix(), self.MAZE_ZERO)
        Dijkstra(graph, self.enter_x, 0)
        banner = (f"╔══════════════════════════════════════════════════════════════════════════╗\n"
                  f"║                           УРОВЕНЬ ПРОЙДЕН                                ║\n"                             
                  f"╚══════════════════════════════════════════════════════════════════════════╝\n"
                  f"════════════════════════════════════════════════════════════════════════════\n"
                  f"Пройденное расстояние: {self.moves_counter}\n"
                  f"Минимально возможное расстояние: {graph.get_vertex(*self.maze.exit_coordinate).distance}\n"
                  f"════════════════════════════════════════════════════════════════════════════\n"
                  f"{self.maze.to_matrix().to_string()}\n"
                  f"════════════════════════════════════════════════════════════════════════════\n")

        items = [




            "Перейти на следующий уровень",
            "Вернуться в главное меню",
            "Выйти",
        ]

        menu = Menu(items, MenuView(), banner)
        self.__maze_width += self.__level_size_increase
        self.__maze_height += self.__level_size_increase

        match menu.get_selected_item():
            case "Вернуться в главное меню":
                self.__current_window = self.__main_menu
            case "Выйти":
                sys.exit()
            case "Перейти на следующий уровень":
                self.__current_window = self.__start_game_cycle

    def __difficulty_settings(self) -> None:
        """
        Отображает меню выбора сложности и обновляет соответствующие настройки игры.
        """
        items = ["Легко",
                 "Сложно"]

        banner = ("╔══════════════════════════════════════════════════════════════════════════╗\n"
                  "║                           НАСТРОЙКИ                                      ║\n"
                  "╚══════════════════════════════════════════════════════════════════════════╝\n")

        main_menu = Menu(items, MenuView(), banner)

        match main_menu.get_selected_item():
            case "Легко":
                self.__level_size_increase = self.EASY_LEVEL_SIZE_INCREASE
                self.__easy_mode = True
            case "Сложно":
                self.__level_size_increase = self.HARD_LEVEL_SIZE_INCREASE
                self.__easy_mode = False

        self.__current_window = self.__main_menu

    def __start_game_cycle(self) -> None:
        """
        Инициализирует и запускает игровой цикл для нового уровня, создавая лабиринт,
        персонажа и обрабатывая вводы пользователя до достижения цели.
        """
        self.enter_x = random.randrange(1, self.__maze_width - 1)
        self.path_builder = MatrixPathBuilder(self.enter_x, 0,
                                              Matrix(self.__maze_width,
                                                     self.__maze_height,
                                                     self.MAZE_ONE,
                                                     self.MAZE_ZERO))
        self.maze = Maze(self.path_builder, 1)
        self.character_view = MatrixCharacterView(self.maze.to_matrix(),
                                                  self.MAZE_UNKNOWN,
                                                  self.MAZE_ZERO,
                                                  self.MAZE_CHARACTER)

        self.character = MatrixCharacter(self.maze.to_matrix(),
                                         self.character_view,
                                         self.enter_x,
                                         0,
                                         self.MAZE_ONE)

        self.moves_counter = 0

        while self.character.position != self.maze.exit_coordinate:

            user_input = keyboard.read_event()

            if user_input.event_type == keyboard.KEY_DOWN:
                if user_input.name == "esc":
                    sys.exit(0)

                if self.character.allowed_move(MOVE_BINDS[user_input.name]):
                    self.moves_counter += 1

                self.character.try_move(MOVE_BINDS[user_input.name])
                Renderer.render(f"Пройденное расстояние: {self.moves_counter}")

                if self.__easy_mode:
                    graph = MatrixGraph(self.maze.to_matrix(), self.MAZE_ZERO)
                    Dijkstra(graph, *self.character.position)
                    Renderer.render(f"Расстояние до выхода: {graph.get_vertex(*self.maze.exit_coordinate).distance}")

        self.__current_window = self.__win
