from Model.Dijkstra.MatrixGraph import MatrixGraph


class Dijkstra:
    """
    Реализует алгоритм Дейкстры для поиска кратчайшего пути в графе,
    представленном в виде матрицы.
    """
    def __init__(self, matrix_graph: MatrixGraph, start_x: int, start_y: int):
        """
        Инициализирует алгоритм Дейкстры с заданным графом и начальной точкой.

        Args:
            matrix_graph: Граф, представленный в виде MatrixGraph.
            start_x: Начальная координата X.
            start_y: Начальная координата Y.
        """
        self.__matrixGraph = matrix_graph
        self.__start_vertex = matrix_graph.get_vertex(start_x, start_y)
        self.__execute()

    def __execute(self) -> None:
        """
        Выполняет алгоритм Дейкстры для поиска кратчайших путей от начальной вершины.
        """
        start_vertex = self.__start_vertex
        graph = self.__matrixGraph
        start_vertex.distance = 0
        non_passed_vertices = [*graph.get_neighbours().keys()]

        while non_passed_vertices:
            current_vertex = min(non_passed_vertices, key=lambda vertex: vertex.distance)
            for neighbour in graph.get_neighbours()[current_vertex]:
                if neighbour in non_passed_vertices and neighbour.distance > current_vertex.distance + 1:
                    neighbour.distance = current_vertex.distance + 1
                    neighbour.set_parent(current_vertex)
            non_passed_vertices.remove(current_vertex)
