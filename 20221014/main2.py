import random


# чтобы удобнее было брать соседние ячейки
costil = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def genlab(width, height, fillpersent):
    # создание пустого массива размерности width x height
    Map = []
    for i in range(height):
        g = []
        for j in range(width):
            g.append(0)
        Map.append(g)

    # случайную точку в массиве закрашиваем (без крайних точек)
    newtons = [(random.randint(1, height - 2), random.randint(1, width - 2))]
    Map[newtons[0][0]][newtons[0][1]] = 1

    tons = newtons.copy()

    s = width * height  # всего ячеек
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

    # первую встретившуюся единицу заменяем двойкой
    # и запоминаем ее позицию
    a = False
    for i in range(height):
        for j in range(width):
            if Map[i][j] == 1:
                Map[i][j] = 2
                a = True
                pos = [i, j]
                break
        if a:
            break

    # последняя встретившаяся единица заменяется тройкой
    a = False
    for i in range(height - 1, 0, -1):
        for j in range(width - 1, 0, -1):
            if Map[i][j] == 1:
                Map[i][j] = 3
                a = True
                break
        if a:
            break

    # возвращаем карту и позицию начала игры
    return Map, pos


graf = {0: "@", 1: "_", 2: "b", 3: "w"}

# функция не используется
def printmap(array, pos):
    for i in range(len(array)):
        a = ""
        for j in range(len(array[0])):
            if i == pos[0] and j == pos[1]:
                a += "p"
            else:
                a += graf.get(array[i][j])
            a += " "
        print(a)


if __name__ == '__main__':
    # ширина 5 клеток, высота 5 клеток, процент заполнения тунелями - 20
    lab, pos = genlab(15, 15, 50)
    # printmap(lab, pos)
    # направление взгляда
    rot = 0
    print("""Ты - крот, который немножко заблудился. Твоя задача - 
на ощупь найти выход из подземных тунелей. 
Ты можешь: двигаться вперед командой - 'w' и поворачивать вправо и 
влево на 90 градусов командами 'r' и 'l' соответственно.
Удачи в поисках выхода.""")
    # пока не дойдем до выхода
    while lab[pos[0]][pos[1]] != 3:
        a = input()
        # если пошли вперед
        if a == "w":
            # если впереди 0 то считаем это стеной
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Впереди стена")
            else:
                print("Ты продвинулся")
                pos[0] += costil[rot][0]
                pos[1] += costil[rot][1]
        # если мы поворачиваемся
        if a == "r":
            rot += 1
            rot %= 4
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Ты повернулся вправо, впереди стена")
            else:
                print("Ты повернулся вправо, впереди нет стены")
        if a == "l":
            rot -= 1
            rot %= 4
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Ты повернулся влево, впереди стена")
            else:
                print("Ты повернулся влево, впереди нет стены")
    print("Ты ПАБЕДИЛ!!!")

