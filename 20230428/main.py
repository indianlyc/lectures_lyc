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
RED_L = (255, 150, 150)
RED_O = (252, 24, 255)  # розовый
RED_C = (255, 154, 24)  # оранжевый
BLUE = (0, 0, 255)
BLUE_L = (150, 150, 255)
BLUE_O = (24, 212, 255)  # голубой
BLUE_C = (127, 24, 255) # фиолетовый


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
        self.name = ""
        self.number = number
        self.x, self.y = xy
        self.color = None
        self.w = WIDTH_OBJECT
        self.h = HEIGHT_OBJECT

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, (self.x*self.w, self.y*self.h, self.w, self.h))

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
            self.w1 = np.random.random((148,150)) - 0.5
            self.w2 = np.random.random((150,100)) - 0.5
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
        alpha = 0.001
        p1 = (np.random.random(self.w1.shape) > 0.999)
        self.w1[p1] += alpha * (np.random.random(self.w1.shape) - 0.5)[p1]

        p2 = (np.random.random(self.w2.shape) > 0.999)
        self.w2[p2] += alpha * (np.random.random(self.w2.shape) - 0.5)[p2]

        p3 = (np.random.random(self.w3.shape) > 0.999)
        self.w3[p3] += alpha * (np.random.random(self.w3.shape) - 0.5)[p3]

        p4 = (np.random.random(self.w4.shape) > 0.999)
        self.w4[p4] += alpha * (np.random.random(self.w4.shape) - 0.5)[p4]

    def get_w(self):
        return self.w1, self.w2, self.w3, self.w4


class Person(GameObject):
    def __init__(self, xy, number, w=None):
        super().__init__(xy, number)
        self.energy = 100
        self.alg = Alg(w=None)
        self.select = False
        self.color_select = None
        self.color_not_select = None
        self.old_color = None
        self.ticks = 0
        self.oldest = False
        self.child = 0
        self.max_child= False
        self.child_color = None

    def add_energy(self, val=1):
        self.energy += 10 * val

    def spend_energy(self):
        self.energy -= 1

    def get_slide(self, a):
        b = np.zeros((7,7))
        for i in range(-3, 4):
            for j in range(-3, 4):
                m = a[(self.x + i) % a.shape[0], (self.y + j) % a.shape[1]]
                if m < 0:
                    m = 0
                b[i + 3, j+ 3] = m
        return b

    def get_move(self, m1, m2, m3):
        a = np.concatenate([self.get_slide(m1).reshape((-1,)),
                            self.get_slide(m2).reshape((-1,)),
                            self.get_slide(m3).reshape((-1,)),
                            np.array([self.energy/100])], axis=0)
        return self.alg.get_move(a)

    def mutation(self):
        self.alg.mutation()

    def get_w(self):
        self.child += 1
        return self.alg.get_w()

    def draw(self, surface):
        self.spend_energy()
        self.ticks += 1

        if self.max_child:
            self.color = self.child_color
        elif self.oldest:
            self.color = self.old_color
        elif self.select:
            self.color = self.color_select
        else:
            self.color = self.color_not_select
        super().draw(surface)


class Grass(GameObject):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "grass"
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
        self.name = "herbivore"
        self.color_not_select = BLUE
        self.color_select = BLUE_L
        self.old_color = BLUE_O
        self.child_color = BLUE_C


class Predator(Person):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "predator"
        self.color_not_select = RED
        self.color_select = RED_L
        self.old_color = RED_O
        self.child_color = RED_C
        self.energy = 100


class World:
    def __init__(self):
        self.count_object = 0
        self.by_n = {}
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
        self.for_stat_object = []

    def create_obj(self, m, Obj):
        res = defaultdict(list)
        for el in np.argwhere(m == 1):
            o = Obj(el, self.count_object)
            res[tuple(el)].append(o)
            self.by_n[self.count_object] = o
            self.count_object += 1
        return res

    def world_logic(self, pos):
        # print(pos)
        if pos is not None:

            list_for_stat = []
            for ep in self.predator_dict[(pos[0]//WIDTH_OBJECT, pos[1]//HEIGHT_OBJECT)]:
                list_for_stat.append(ep.number)
            for eh in self.herbivore_dict[(pos[0]//WIDTH_OBJECT, pos[1]//HEIGHT_OBJECT)]:
                list_for_stat.append(eh.number)
            if len(list_for_stat):
                for id in self.for_stat_object:
                    if self.by_n.get(id, False):
                        self.by_n[id].select = False
                self.for_stat_object = []
                for id in list_for_stat:
                    self.by_n[id].select = True
                self.for_stat_object = list_for_stat
            print(pos, (pos[0]//WIDTH_OBJECT, pos[1]//HEIGHT_OBJECT),
                  self.for_stat_object,
                  [self.by_n[id].energy for id in self.for_stat_object if self.by_n.get(id, False)])

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
            for o in self.herbivore_dict[el]:
                del self.by_n[o.number]
            del self.herbivore_dict[el]
            count_pred = len(self.predator_dict[el])
            for ep in self.predator_dict[el]:
                ep.add_energy(val=count_herb/count_pred)

        for id in list(self.by_n.keys()):
            o = self.by_n[id]
            if o.name in ["herbivore", "predator"]:
                if o.energy <= 0:
                    xy = o.x, o.y
                    if o.name == "herbivore":
                        self.herbivore[xy] -= 1
                        self.herbivore_dict[xy].remove(o)
                    else:
                        self.predator[xy] -= 1
                        self.predator_dict[xy].remove(o)
                    del self.by_n[id]


    def move(self):
        dd_h = np.sum(np.sum(self.herbivore)) <= 20
        # dd = sum([len(el) for el in self.herbivore_dict.values()]) <= 10
        if dd_h:
            self.herbivore_deaded_count += 1

        dd_p = np.sum(np.sum(self.predator)) <= 20
        # dd = sum([len(el) for el in self.predator_dict.values()]) <= 10
        if dd_p:
            self.predator_deaded_count += 1

        for id in list(self.by_n.keys()):
            o = self.by_n[id]
            if o.name in ["herbivore", "predator"]:
                delta = o.get_move(self.grass, self.herbivore, self.predator)
                xy = o.x, o.y
                o.x += delta[0]
                o.x = o.x % (WIDTH//WIDTH_OBJECT)
                o.y += delta[1]
                o.y = o.y % (HEIGHT//HEIGHT_OBJECT)
                new_xy = o.x, o.y
                if o.name == "herbivore":
                    self.herbivore[xy] -= 1
                    self.herbivore[new_xy] += 1
                    self.herbivore_dict[xy].remove(o)
                    self.herbivore_dict[new_xy].append(o)
                    if o.energy >= 200 or dd_h:
                        if o.energy >= 200:
                            o.energy -= 100
                        else:
                            o.energy = 100
                            o.ticks = 0
                        new_h = Herbivore(xy, self.count_object, w=o.get_w())
                        new_h.mutation()
                        self.by_n[self.count_object] = new_h
                        self.herbivore_dict[xy].append(new_h)
                        self.count_object += 1
                        self.herbivore[xy] += 1
                else:
                    self.predator[xy] -= 1
                    self.predator[new_xy] += 1
                    self.predator_dict[xy].remove(o)
                    self.predator_dict[new_xy].append(o)
                    if o.energy >= 200 or dd_p:
                        if o.energy >= 200:
                            o.energy -= 100
                        else:
                            o.energy = 100
                            o.ticks = 0
                        new_p = Predator(xy, self.count_object, w=o.get_w())
                        new_p.mutation()
                        self.by_n[self.count_object] = new_p
                        self.predator_dict[xy].append(new_p)
                        self.count_object += 1
                        self.predator[xy] += 1

    def get_stat(self):
        hm = self.by_n[max([(self.by_n[id].ticks, id) for id in self.by_n if self.by_n[id].name == "herbivore"])[1]]
        pm = self.by_n[max([(self.by_n[id].ticks, id) for id in self.by_n if self.by_n[id].name == "predator"])[1]]
        for id in self.by_n:
            self.by_n[id].oldest= False
        hm.oldest = True
        pm.oldest = True

        hc = self.by_n[max([(self.by_n[id].child, id) for id in self.by_n if self.by_n[id].name == "herbivore"])[1]]
        pc = self.by_n[max([(self.by_n[id].child, id) for id in self.by_n if self.by_n[id].name == "predator"])[1]]
        for id in self.by_n:
            self.by_n[id].max_child= False
        hc.max_child = True
        pc.max_child = True

        return (
                np.sum(np.sum(self.grass[self.grass > 0])),
                np.sum(np.sum(self.herbivore)),
                np.sum(np.sum(self.predator)),
                sum([eh.energy for el in self.herbivore_dict.values() for eh in el]),
                sum([ep.energy for el in self.predator_dict.values() for ep in el]),
                self.herbivore_deaded_count,
                self.predator_deaded_count,
                str([{"xy": (self.by_n[el].x, self.by_n[el].y),
                      "energy": round(self.by_n[el].energy),
                      "ticks": self.by_n[el].ticks,
                      "child": self.by_n[el].child,
                      "number": self.by_n[el].number,
                      "name": self.by_n[el].name,}\
                            for el in self.for_stat_object if self.by_n.get(el, False)]),
                str({
                    "xy": (hm.x, hm.y),
                    "energy": round(hm.energy),
                    "child": hm.child,
                     "ticks": hm.ticks,
                    "number": hm.number,
                    "name": hm.name,
                     }),
                str({
                    "xy": (pm.x, pm.y),
                    "energy": round(pm.energy),
                    "child": pm.child,
                     "ticks": pm.ticks,
                    "number": pm.number,
                    "name": pm.name,
                }),
                str({
                    "xy": (hc.x, hc.y),
                    "energy": round(hc.energy),
                    "child": hc.child,
                     "ticks": hc.ticks,
                    "number": hc.number,
                    "name": hc.name,
                }),
                str({
                    "xy": (pc.x, pc.y),
                    "energy": round(pc.energy),
                    "child": pc.child,
                     "ticks": pc.ticks,
                    "number": pc.number,
                    "name": pc.name,
                }),
                )

            # (sum([len(el) for el in self.grass_dict.values() if len(el) and not el[0].imeat]),
            #     sum([len(el) for el in self.herbivore_dict.values()]),
            #     sum([len(el) for el in self.predator_dict.values()]),


class WorldEvolution:
    def __init__(self):
        self._init_pygame()
        pygame.font.init()
        self.font = pygame.font.SysFont('Comic Sans MS', 30)
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
        self.x8 = ""
        self.x9 = ""
        self.x10 = ""
        self.x11 = ""
        self.x12 = ""
        self.pos = None

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
            if event.type == pygame.MOUSEBUTTONUP:
                self.pos = pygame.mouse.get_pos()
                # print(self.pos)
            else:
                self.pos = None
            if event.type == pygame.QUIT or (
                event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
            ):
                quit()

    def _process_game_logic(self):
        self.world.world_logic(self.pos)
        self.world.move()
        x1,x2,x3,x4,x5,x6,x7,self.x8, self.x9, self.x10, self.x11,self.x12 = self.world.get_stat()
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

        self.screen.blit(self.font.render(self.x8, False, WHITE), (1050, 800))
        self.screen.blit(self.font.render(self.x9, False, WHITE), (1050, 840))
        self.screen.blit(self.font.render(self.x10, False, WHITE), (1050, 880))
        self.screen.blit(self.font.render(self.x11, False, WHITE), (1050, 920))
        self.screen.blit(self.font.render(self.x12, False, WHITE), (1050, 960))


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