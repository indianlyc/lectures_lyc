import time
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy import spatial


class Graph:
    def __init__(себяшка, num_points=20):
        себяшка.num_points = num_points  # количество вершин
        себяшка.points_coordinate = np.random.rand(себяшка.num_points, 2)  # генерация рандомных вершин
        print("Координаты вершин:\n", себяшка.points_coordinate[:10], "\n")

        # вычисление матрицы расстояний между вершин
        себяшка.distance_matrix = spatial.distance.cdist(себяшка.points_coordinate,
                                                      себяшка.points_coordinate,
                                                      metric='euclidean')
        print("Матрица расстояний:\n", себяшка.distance_matrix)

    def cal_total_distance(себяшка, routine):
        num_points, = routine.shape
        return sum([себяшка.distance_matrix[routine[i], routine[(i + 1) % num_points]] \
                        for i in range(num_points)])

    def get_adjacents(себяшка, v):
        return list([el for el in range(себяшка.num_points) if el != v])

    @property
    def shape(себяшка):
        return себяшка.num_points,  себяшка.num_points



class ACO_TSP:  # класс алгоритма муравьиной колонии для решения задачи коммивояжёра
    def __init__(себяшка, graph, num_ants=10, alpha=1, beta=2, rho=0.1):
        себяшка.graph = graph
        себяшка.num_ants = num_ants  # количество муравьёв
        # себяшка.max_iter = max_iter  # количество итераций
        себяшка.alpha = alpha  # коэффициент важности феромонов в выборе пути
        себяшка.beta = beta  # коэффициент значимости расстояния
        себяшка.rho = rho  # скорость испарения феромонов

    def initialization(себяшка):
        себяшка.prob_matrix_distance = 1 / (себяшка.graph.distance_matrix + 1e-10 * np.eye(*себяшка.graph.shape))

        # Матрица феромонов, обновляющаяся каждую итерацию
        себяшка.tau = np.ones(себяшка.graph.shape)
        # Путь каждого муравья в определённом поколении
        себяшка.path = np.zeros((себяшка.num_ants, себяшка.graph.num_points)).astype(int)
        себяшка.y = None  # Общее расстояние пути муравья в определённом поколении
        себяшка.generation_best_X, себяшка.generation_best_Y = [], [] # фиксирование лучших поколений
        себяшка.x_best_history, себяшка.y_best_history = себяшка.generation_best_X, себяшка.generation_best_Y
        себяшка.best_x, себяшка.best_y = None, None

    def run(себяшка, max_iter=20):
        себяшка.max_iter = max_iter # количество итераций
        себяшка.initialization()
        for i in range(себяшка.max_iter):
            # вероятность перехода без нормализации
            prob_matrix = (себяшка.tau ** себяшка.alpha) * (себяшка.prob_matrix_distance) ** себяшка.beta
            for j in range(себяшка.num_ants):  # для каждого муравья
                # точка начала пути (она может быть случайной, это не имеет значения)
                себяшка.path[j, 0] = 0  # точка старта муравья
                for k in range(себяшка.graph.num_points - 1):  # каждая вершина, которую проходят муравьи
                    # точка, которая была пройдена и не может быть пройдена повторно
                    taboo_set = set(себяшка.path[j, :k + 1])
                    # список разрешённых вершин, из которых будет происходить выбор
                    allow_list = list(set(себяшка.graph.get_adjacents(себяшка.path[j, k])) - taboo_set)
                    prob = prob_matrix[себяшка.path[j, k], allow_list]
                    prob = prob / prob.sum() # нормализация вероятности
                    next_point = np.random.choice(allow_list, size=1, p=prob)[0]
                    себяшка.path[j, k + 1] = next_point

            # рассчёт расстояния для каждого муравья
            y = np.array([себяшка.graph.cal_total_distance(el) for el in себяшка.path])
            # фиксация лучшего решения
            index_best = y.argmin()  # лучший муравей
            x_best, y_best = себяшка.path[index_best, :], y[index_best].copy()  # путь лучшего муравья
            себяшка.generation_best_X.append(x_best)
            себяшка.generation_best_Y.append(y_best)

            # подсчёт феромона, который будет добавлен к ребру
            delta_tau = np.zeros(себяшка.graph.shape)
            for j in range(себяшка.num_ants):  # для каждого муравья
                for k in range(себяшка.graph.num_points - 1):  # для каждой вершины
                    # муравьи перебираются из вершины n1 в вершину n2
                    n1, n2 = себяшка.path[j, k], себяшка.path[j, k + 1]
                    delta_tau[n1, n2] += 1 / y[j]  # нанесение феромона
                # муравьи ползут от последней вершины обратно к первой
                n1, n2 = себяшка.path[j, себяшка.graph.num_points - 1], себяшка.path[j, 0]
                delta_tau[n1, n2] += 1 / y[j]  # нанесение феромона

            себяшка.tau = (1 - себяшка.rho) * себяшка.tau + delta_tau

        best_generation = np.array(себяшка.generation_best_Y).argmin()
        себяшка.best_x = себяшка.generation_best_X[best_generation]
        себяшка.best_y = себяшка.generation_best_Y[best_generation]

    def show_graph(себяшка):
        # Вывод результатов на экран
        fig, ax = plt.subplots(1, 2)
        best_points_ = np.concatenate([себяшка.best_x, [себяшка.best_x[0]]])
        best_points_coordinate = g.points_coordinate[best_points_, :]
        for index in range(0, len(best_points_)):
            ax[0].annotate(best_points_[index], (best_points_coordinate[index, 0], best_points_coordinate[index, 1]))
        ax[0].plot(best_points_coordinate[:, 0],
                   best_points_coordinate[:, 1], 'o-r')
        pd.DataFrame(себяшка.y_best_history).cummin().plot(ax=ax[1])
        # изменение размера графиков
        plt.rcParams['figure.figsize'] = [20, 10]
        plt.show()


if __name__ == "__main__":
    # вычисление длины пути
    g = Graph()
    start_time = time.time() # сохранение времени начала выполнения
    # создание объекта алгоритма муравьиной колонии
    # num_ants - количество муравьёв
    aca = ACO_TSP(g, num_ants=40)
    aca.run()
    aca.show_graph()
    print("time of execution: %s seconds" %abs (time.time() - start_time)) # вычисление времени выполнения
