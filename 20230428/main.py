from collections import defaultdict
import pygame
import random
import numpy as np
from numpy.lib.stride_tricks import sliding_window_view

import matplotlib
matplotlib.use("Agg")

import matplotlib.backends.backend_agg as agg
import pylab
import matplotlib.pyplot as plt

from copy import copy, deepcopy


plt.rcParams.update({
    #"lines.marker": "o",         # available ('o', 'v', '^', '<', '>', '8', 's', 'p', '*', 'h', 'H', 'D', 'd', 'P', 'X')
    "lines.linewidth": "1.8",
    "axes.prop_cycle": plt.cycler('color', ['white']),  # line color
    "text.color": "white",       # no text in this example
    "axes.facecolor": "black",   # background of the figure
    "axes.edgecolor": "lightgray",
    "axes.labelcolor": "white",  # no labels in this example
    "axes.grid": "True",
    "grid.linestyle": "--",      # {'-', '--', '-.', ':', '', (offset, on-off-seq), ...}
    "xtick.color": "white",
    "ytick.color": "white",
    "grid.color": "lightgray",
    "figure.facecolor": "black", # color surrounding the plot
    "figure.edgecolor": "black",
})


WIDTH = 1000
HEIGHT = 1000
WIDTH_OBJECT = 10
HEIGHT_OBJECT = 10
FPS = 60
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)


class GraphicObject:
    def __init__(self, *args):
        self.fig = pylab.figure(figsize=[4, 4],  # Inches
                           dpi=100,  # 100 dots per inch, so the resulting buffer is 400x400 pixels
                           )
        self.ax = self.fig.gca()
        self.ax.plot(*args)

        self.canvas = agg.FigureCanvasAgg(self.fig)
        self.canvas.draw()
        self.renderer = self.canvas.get_renderer()
        self.raw_data = self.renderer.tostring_rgb()
        plt.close()

    def draw(self,screen, x=1050, y=0):
        # screen = pygame.display.get_surface()
        size = self.canvas.get_width_height()
        surface = pygame.image.fromstring(self.raw_data, size, "RGB")
        screen.blit(surface, (x, y))


class GameObject:
    def __init__(self, xy, number):
        self.number = number
        self.x, self.y = xy
        self.color = None
        self.w = WIDTH_OBJECT
        self.h = HEIGHT_OBJECT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x*self.w, self.y*self.h, self.w, self.h), border_radius=2)

    def __eq__(self, other):
        return other.number == self.number

d_move = {
            0: np.array((0, 0)),  # стоять на месте
            1: np.array((0, 1)),  # идти вниз
            2: np.array((1, 0)),  # идти вправо
            3: np.array((0, -1)), # идти вверх
            4: np.array((-1, 0)),  # идти вниз
            5: np.array((1, 1)),   # вправо-вниз
            6: np.array((-1, -1)),  # влево-вверх
            7: np.array((-1, 1)),  # влево-вниз
            8: np.array((1, -1)),  # вправо-вверх
        }

class Alg:
    def __init__(self, w=None):
        if w is None:
            self.w1 = np.random.random((76,100)) - 0.5
            self.w2 = np.random.random((100,100)) - 0.5
            self.w3 = np.random.random((100,20)) - 0.5
            self.w4 = np.random.random((20, 9)) - 0.5


            # 7600 + 10000 + 2000 + 180
        else:
            self.w1, self.w2, self.w3, self.w4 = w
        self.last_move = None

    def sigmoid(self, Z):
        return 1 / (1 + np.exp(-Z))

    def get_move(self, a):

        r = self.sigmoid(self.sigmoid(self.sigmoid(a.dot(self.w1))\
                                    .dot(self.w2)).dot(self.w3)).dot(self.w4)
        rr = np.where(r == np.max(r))[0][0]
        return d_move[rr]

    def mutation(self):
        p1 = (np.random.random(self.w1.shape) > 0.99).astype(int)
        self.w1[p1] = (np.random.random(self.w1.shape) - 0.5)[p1]

        p2 = (np.random.random(self.w2.shape) > 0.99).astype(int)
        self.w2[p2] = (np.random.random(self.w2.shape) - 0.5)[p2]

        p3 = (np.random.random(self.w3.shape) > 0.99).astype(int)
        self.w3[p3] = (np.random.random(self.w3.shape) - 0.5)[p3]

        p4 = (np.random.random(self.w4.shape) > 0.99).astype(int)
        self.w4[p4] = (np.random.random(self.w4.shape) - 0.5)[p4]

    def get_w(self):
        return self.w1, self.w2, self.w3, self.w4


class Person(GameObject):
    def __init__(self, xy, number, w=None):
        super().__init__(xy, number)
        self.energy = 100
        self.alg = Alg(w=None)

    def add_energy(self, val=1):
        self.energy += 10 * val

    def spend_energy(self):
        self.energy -= 1

    def get_slide(self, a):
        b = np.zeros((5,5))
        for i in range(-2, 3):
            for j in range(-2, 3):
                m = a[(self.x + i) % a.shape[0], (self.y + j) % a.shape[1]]
                if m < 0:
                    m = 0
                b[i + 2, j+ 2] = m
        return b

    def get_move(self, m1, m2, m3):
        a = np.concatenate([self.get_slide(m1).reshape((-1,)),
                            self.get_slide(m2).reshape((-1,)),
                            self.get_slide(m3).reshape((-1,)),
                            np.array([self.energy/100])], axis=0)
        self.spend_energy()
        return self.alg.get_move(a)

    def mutation(self):
        self.alg.mutation()

    def get_w(self):
        return self.alg.get_w()


class Grass(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = GREEN
        self.count = 0
        self.imeat = False

    def eat(self):
        self.imeat = True
        self.count = 150

    def draw(self, surface):
        if not self.imeat:
            super().draw(surface)
        else:
            self.count -= 1
            if self.count <= 0:
                self.imeat = False



class Herbivore(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = BLUE


class Predator(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.color = RED
        self.energy = 100


class World:
    def __init__(self):
        self.count_object = 0
        self.shape = (WIDTH//WIDTH_OBJECT, HEIGHT//HEIGHT_OBJECT)
        # self.field = np.zeros(self.shape)
        self.grass = (np.random.random(self.shape) > 0.20).astype(int)
        self.grass_dict = self.create_obj(self.grass, Grass)
        self.herbivore = (np.random.random(self.shape) > 0.80).astype(int)
        self.herbivore_dict = self.create_obj(self.herbivore, Herbivore)
        self.predator = (np.random.random(self.shape) > 0.95).astype(int)
        self.predator_dict = self.create_obj(self.predator, Predator)
        self.herbivore_deaded_count = 0
        self.predator_deaded_count = 0

    def create_obj(self, m, Obj):
        res = defaultdict(list)
        for el in np.argwhere(m == 1):
            res[tuple(el)].append(Obj(el, self.count_object))
            self.count_object += 1
        return res

    def world_logic(self):
        for el in np.argwhere(self.grass == -1):
            el = tuple(el)
            for eg in self.grass_dict[el]:
                if not eg.imeat:
                    self.grass[el] = len(self.grass_dict[el])

        for el in np.argwhere((self.grass > 0) & (self.herbivore > 0)):
            el = tuple(el)
            # print("del grass", el)
            self.grass[el] = -1
            count_grass = len(self.grass_dict[el])
            for grass in self.grass_dict[el]:
                grass.eat()
            count_herb = len(self.herbivore_dict[el])
            for eh in self.herbivore_dict[el]:
                eh.add_energy(val=count_grass/count_herb)

        for el in np.argwhere((self.herbivore > 0) & (self.predator > 0)):
            el = tuple(el)
            # print("del herbivore", el)
            self.herbivore[el] = 0
            count_herb = sum([kp.energy for kp in  self.herbivore_dict[el]])/20
            del self.herbivore_dict[el]
            count_pred = len(self.predator_dict[el])
            for ep in self.predator_dict[el]:
                ep.add_energy(val=count_herb/count_pred)

        key_list = list(self.herbivore_dict)
        for xy in key_list:
            for i, eh in enumerate(self.herbivore_dict[xy]):
                if eh.energy <= 0:
                    # print("null energy herbivore", xy)
                    self.herbivore[xy] -= 1
                    self.herbivore_dict[xy].remove(eh)

        key_list = list(self.predator_dict)
        for xy in key_list:
            for i, ep in enumerate(self.predator_dict[xy]):
                if ep.energy <= 0:
                    # print("null energy herbivore", xy)
                    self.predator[xy] -= 1
                    self.predator_dict[xy].remove(ep)

    def move(self):
        dd = np.sum(np.sum(self.herbivore)) <= 20
        # dd = sum([len(el) for el in self.herbivore_dict.values()]) <= 10
        if dd:
            self.herbivore_deaded_count += 1

        list_herbivore = deepcopy(self.herbivore_dict).items()
        for xy, el in list_herbivore:
            for i, eh in enumerate(el):
                delta = eh.get_move(self.grass, self.herbivore, self.predator)
                self.herbivore[xy] -= 1
                eh.x += delta[0]
                eh.x = eh.x % (WIDTH//WIDTH_OBJECT)
                eh.y += delta[1]
                eh.y = eh.y % (HEIGHT//HEIGHT_OBJECT)
                self.herbivore[(eh.x, eh.y)] += 1
                self.herbivore_dict[xy].remove(eh)
                self.herbivore_dict[(eh.x, eh.y)].append(eh)
                if eh.energy >= 200 or dd:
                    if eh.energy >= 200:
                        eh.energy -= 100
                    else:
                        eh.energy = 100
                    new_h = Herbivore(xy, self.count_object, w=eh.get_w())
                    new_h.mutation()
                    self.herbivore_dict[xy].append(new_h)
                    self.count_object += 1
                    self.herbivore[xy] += 1

        dd = np.sum(np.sum(self.predator)) <= 20
        # dd = sum([len(el) for el in self.predator_dict.values()]) <= 10
        if dd:
            self.predator_deaded_count += 1

        list_predator = deepcopy(self.predator_dict).items()
        for xy, el in list_predator:
            for i, ep in enumerate(el):
                delta = ep.get_move(self.grass, self.herbivore, self.predator)
                self.predator[xy] -= 1
                ep.x += delta[0]
                ep.x = ep.x % (WIDTH//WIDTH_OBJECT)
                ep.y += delta[1]
                ep.y = ep.y % (HEIGHT//HEIGHT_OBJECT)
                self.predator[(ep.x, ep.y)] += 1
                self.predator_dict[xy].remove(ep)
                self.predator_dict[(ep.x, ep.y)].append(ep)
                if ep.energy >= 200 or dd:
                    if ep.energy >= 200:
                        ep.energy -= 100
                    else:
                        ep.energy = 100
                    new_p = Predator(xy, self.count_object, w=ep.get_w())
                    new_p.mutation()
                    self.predator_dict[xy].append(new_p)
                    self.count_object += 1
                    self.predator[xy] += 1

    def get_stat(self):
        return (
                np.sum(np.sum(self.grass[self.grass > 0])),
                np.sum(np.sum(self.herbivore)),
                np.sum(np.sum(self.predator)),
                sum([eh.energy for el in self.herbivore_dict.values() for eh in el]),
                sum([ep.energy for el in self.predator_dict.values() for ep in el]),
                self.herbivore_deaded_count,
                self.predator_deaded_count
                )

            # (sum([len(el) for el in self.grass_dict.values() if len(el) and not el[0].imeat]),
            #     sum([len(el) for el in self.herbivore_dict.values()]),
            #     sum([len(el) for el in self.predator_dict.values()]),


class WorldEvolution:
    def __init__(self):
        self._init_pygame()
        self.screen = pygame.display.set_mode((WIDTH+850, HEIGHT))
        self.background = BLACK
        self.clock = pygame.time.Clock()
        self.world = World()
        self.k = 0
        self.x_list = []
        self.x1_list = []
        self.x2_list = []
        self.x3_list = []
        self.x4_list = []
        self.x5_list = []
        self.x6_list = []
        self.x7_list = []

    def main_loop(self):
        while True:
            self.clock.tick(FPS)
            self._handle_input()
            self._process_game_logic()
            self._draw()

    def _init_pygame(self):
        pygame.init()
        pygame.display.set_caption("Эволюция!")

    def _handle_input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

    def _process_game_logic(self):
        self.world.world_logic()
        self.world.move()
        x1,x2,x3,x4,x5,x6,x7 = self.world.get_stat()
        self.x1_list.append(x1)
        self.x2_list.append(x2)
        self.x3_list.append(x3)
        self.x4_list.append(x4)
        self.x5_list.append(x5)
        self.x6_list.append(x6)
        self.x7_list.append(x7)
        self.x_list.append(self.k)
        self.k += 1

    def _draw(self):
        self.screen.fill(self.background)
        for el in self.world.grass_dict.values():
            for eg in el:
                eg.draw(self.screen)
        for el in self.world.herbivore_dict.values():
            for eh in el:
                eh.draw(self.screen)
        for el in self.world.predator_dict.values():
            for ep in el:
                ep.draw(self.screen)
        GraphicObject(self.x_list, self.x1_list, "green",
                      self.x_list, self.x2_list, "blue",
                      self.x_list, self.x3_list, "red").draw(self.screen, 1030, 0)

        GraphicObject(self.x_list[-100:], self.x1_list[-100:], "green",
                      self.x_list[-100:], self.x2_list[-100:], "blue",
                      self.x_list[-100:], self.x3_list[-100:], "red").draw(self.screen, 1030, 400)

        GraphicObject(self.x_list, self.x6_list, "blue",
                      self.x_list, self.x7_list, "red",).draw(self.screen, 1450, 0)

        GraphicObject(self.x_list, self.x4_list, "blue",
                      self.x_list, self.x5_list, "red",).draw(self.screen, 1450, 400)
        pygame.display.flip()


if __name__ == "__main__":
    world_evolution = WorldEvolution()
    world_evolution.main_loop()


# 1. Подписать графики и оси на них
# 2. Изменить название x_list, x итд. , сделать d_move статическим свойством класса
# 3. Выделить те константы которые являются параметрами в отдельные переменные.
#                      Подобрать параметры чтобы не вымирали (не факт что получится)
# 4. Сделать вывод информации о квадратике в правый нижний угол при наведении на него мышкой:
#                         номер, тип, сколько циклов живет, какая энергия
# 5. Выводить внизу еще правее - максимальную длинну жизни травоядного и хищника, максимальную энергию,
#                         общее количество травы, травоядных, хищников в текущий момент времени.
# 6. Написать алгоритм для хищников, который бы выигрывал хищников по-умолчанию и не вымирал
#        изначально 1, но может размножаться. (не изменяется при наследовании)
# 7. Написать алгоритм для травоядных который бы выигрывал травоядных по-умолчанию и не вымирал
#        изначально 1, но может размножаться. (не изменяется при наследовании)
# 8. Расширить поле видимости с 5на5 до 7 на 7.
# 9. Добавить возможность играть за травоядного или хищника и сохранять при этом что получает на вход нейросеть и ваш ход

# 1,2,[3] - 1 бал
# 4,5 - 1 бал
# 6 - 1 бал
# 7,8 - 1 бал
# 9 - 1 бал