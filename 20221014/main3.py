from random import randint
from random import shuffle
import numpy as np


class InputCommon:
    def input(self):
        return input()


class OutputCommon:
    def output(self, val):
        print(val)


class Hero:
    def __init__(self, pos):
        self.pos = pos
        self.rot = 0
        # чтобы удобнее было брать соседние ячейки
        self._costil = np.array([(1, 0), (0, -1), (-1, 0), (0, 1)])

    def right(self):
        self.rot += 1
        self.rot %= 4

    def left(self):
        self.rot -= 1
        self.rot %= 4

    def forward(self):
        self.pos += self._costil[self.rot]

    @property
    def forward_pos(self):
        return self.pos + self._costil[self.rot]


class Lab:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.shape = (width, height)
        self.map = np.zeros(self.shape, dtype=np.uint8)
        self.start_pos = np.array([randint(1, width - 2), randint(1, height - 2)])
        self.map[self.start_pos] = 1

    def on_finish(self, hero: Hero) -> bool:
        return self.map[hero.pos] == 3

    def forward_info(self, hero: Hero):
        return self.map[hero.forward_pos]

    @property
    def count_cells(self):
        return self.width * self.height


class Way:
    def __init__(self, xy, width, height):
        self.width = width
        self.height = height
        self.set_cells = {xy}
        self.last = [xy]
        self._costil = np.array([(1, 0), (0, -1), (-1, 0), (0, 1)])

    def get_good_cell(self,xy):
        for v in self._costil:
            cell = xy + v
            # if проверка на не выход
        return cell


    def add_cell(self):
        while True:
            xy = self.last.pop()
            shuffle(self._costil)
            cell = self.get_good_cell(xy)
            self.set_cells.add(cell)
            self.last.append(cell)
            yield





class GenerateLab:
    def __init__(self, width: int, height: int, fill_persent: int):
        self.lab: Lab = Lab(width, height)
        self.fill_persent: int = fill_persent
        self.tons = None
        self._costil = np.array([(1, 0), (0, -1), (-1, 0), (0, 1)])

    def into_map(self, x,y):
        return 0 < x < self.lab.height - 1 and 0 < y < self.lab.width - 1

    def get_new_tons(self, newtons):
        newnewtons = []
        for i in range(len(newtons)):

            # считаем сколько нулей вокруг текущей ячейки
            m = []
            for k in range(len(self._costil)):
                if self.map[newtons[i] + self._costil[k]] == 0:
                    # запоминаем в какую сторону был ноль
                    m.append(k)

            h = 0
            while m:
                # берем случайную сторону с нулем
                a = randint(0, len(m) - 1)
                # если мы еще в этом цикле не добавили единицы к массиву
                # и ноль был только в одну сторону
                # или с вероятностью 1/100 заходим в условие
                if (h == 0 and len(m) == 1) or randint(0, 100) == 1:
                    # запомнили координаты точки с нулем
                    bc = newtons[i] + self._costil[m[a]]

                    # если она попадает в массив (без крайних точек)
                    if self.into_map(*bc):
                        # то запоминаем кто из ее соседей закрашена единицей
                        f = []
                        for k in range(len(self._costil)):
                            if self.map[bc + self._costil[k]] == 1:
                                f.append(k)

                        # если такой сосед всего один
                        if len(f) == 1:
                            # то наша нулевая точка продолжение пути
                            self.map[bc] = 1
                            # запоминаем ее
                            newnewtons.append(bc)
                            h += 1
                        # если таких соседа два
                        elif len(f) == 2:
                            # и соседи на противоположных сторонах
                            d = abs(f[0] - f[1])
                            if d == 2:
                                # соединяем их окрашивая в единицу
                                self.map[bc] = 1
                                newnewtons.append(bc)
                                h += 1
                            # если соседи 90 градусов друг другу
                            else:
                                # и еще не соединены
                                if self.map[bc + self._costil[f[0]] + self._costil[f[1]]] == 0:
                                    # соединяем их
                                    self.map[bc] = 1
                                    newnewtons.append(bc)
                                    h += 1
                # обработали сторону с нулем забываем про нее
                m.pop(a)

        for i in range(len(newtons)):
            if not newtons[i] in self.tons:
                self.tons.append(newtons[i])
        return newtons

    def generate(self):
        newtons = [self.lab.start_pos]
        self.tons = newtons.copy()

        s = self.lab.count_cells
        while len(self.tons) / s < self.fillpersent / 100:  # пока не закрасим нужный процент точек
            while newtons:
                newtons = self.get_new_tons(newtons)

            # если мы не нашли ячейку для окраски
            # то стартуем с рандомной точки в нашем пути
            newtons = [self.tons[randint(0, len(self.tons) - 1)]]

        return self.lab

    def init(self):
        self.map = []
        for i in range(self.height):
            g = []
            for j in range(self.width):
                g.append(0)
        self.map.append(g)


class Game:
    def __init__(self):
        self.__intro = """Ты - крот, который немножко заблудился. Твоя задача - 
на ощупь найти выход из подземных тунелей. 
Ты можешь: двигаться вперед командой - 'w' и поворачивать вправо и 
влево на 90 градусов командами 'r' и 'l' соответственно.
Удачи в поисках выхода."""
        self.out = OutputCommon()
        self.input = InputCommon()
        self.do_dict = {
            "w": self.do_forward,
            "r": self.do_right,
            "l": self.do_left,
        }
        self.hero = None
        self.lab = None
        self.wall_signal = 0

    def _intro(self):
        self.out.output(self.__intro)

    def is_wall(self):
        return self.lab.forward_info(self.hero) == self.wall_signal

    def do_forward(self):
        # если впереди 0 то считаем это стеной
        if self.is_wall():
            self.out.output("Впереди стена")
        else:
            self.out.output("Ты продвинулся")
            self.hero.forward()

    def do_right(self):
        self.hero.right()
        if self.is_wall():
            self.out.output("Ты повернулся вправо, впереди стена")
        else:
            self.out.output("Ты повернулся вправо, впереди нет стены")

    def do_left(self):
        self.hero.left()
        if self.is_wall():
            self.out.output("Ты повернулся влево, впереди стена")
        else:
            self.out.output("Ты повернулся влево, впереди нет стены")

    def win(self):
        self.out.output("Ты ПАБЕДИЛ!!!")

    def start(self):
        self._intro()
        # ширина 5 клеток, высота 5 клеток, процент заполнения тунелями - 20
        self.lab = GenerateLab(15, 15, 50).generate()
        self.hero = Hero(self.lab.start_pos)
        # пока не дойдем до выхода
        while not self.lab.on_finish(self.hero):
            a = ""
            while a not in self.do_dict:
                a = self.input.input()
            self.do_dict[a]()
        self.win()


def genlab(width, height, fillpersent):

    while len(tons) / s < fillpersent / 100: # пока не закрасим нужный процент точек
        while newtons:
            newnewtons = []
            for i in range(len(newtons)):

                # считаем сколько нулей вокруг текущей ячейки
                m = []
                for k in range(len(costil)):
                    if Map[newtons[i][0] + costil[k][0]][newtons[i][1] + costil[k][1]] == 0:
                        # запоминаем в какую сторону был ноль
                        m.append(k)

                h = 0
                while m:
                    # берем случайную сторону с нулем
                    a = random.randint(0, len(m) - 1)
                    # если мы еще в этом цикле не добавили единицы к массиву
                    # и ноль был только в одну сторону
                    # или с вероятностью 1/100 заходим в условие
                    if (h == 0 and len(m) == 1) or random.randint(0, 100) == 1:
                        # запомнили координаты точки с нулем
                        b = newtons[i][0] + costil[m[a]][0]
                        c = newtons[i][1] + costil[m[a]][1]

                        # если она попадает в массив (без крайних точек)
                        if 0 < b < height - 1 and 0 < c < width - 1:
                            # то запоминаем кто из ее соседей закрашена единицей
                            f = []
                            for k in range(len(costil)):
                                if Map[b + costil[k][0]][c + costil[k][1]] == 1:
                                    f.append(k)

                            # если такой сосед всего один
                            if len(f) == 1:
                                # то наша нулевая точка продолжение пути
                                Map[b][c] = 1
                                # запоминаем ее
                                newnewtons.append((b, c))
                                h += 1
                            # если таких соседа два
                            elif len(f) == 2:
                                # и соседи на противоположных сторонах
                                d = abs(f[0] - f[1])
                                if d == 2:
                                    # соединяем их окрашивая в единицу
                                    Map[b][c] = 1
                                    newnewtons.append((b, c))
                                    h += 1
                                # если соседи 90 градусов друг другу
                                else:
                                    # и еще не соединены
                                    if Map[b + costil[f[0]][0] + costil[f[1]][0]][
                                        c + costil[f[0]][1] + costil[f[1]][1]] == 0:
                                        # соединяем их
                                        Map[b][c] = 1
                                        newnewtons.append((b, c))
                                        h += 1
                    # обработали сторону с нулем забываем про нее
                    m.pop(a)

            for i in range(len(newtons)):
                if not newtons[i] in tons:
                    tons.append(newtons[i])
            newtons = newnewtons

        # если мы не нашли ячейку для окраски
        # то стартуем с рандомной точки в нашем пути
        newtons = [tons[random.randint(0, len(tons) - 1)]]




if __name__ == '__main__':
    game = Game()
    game.start()

