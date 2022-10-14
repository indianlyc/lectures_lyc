import random

costil = [(1, 0), (0, -1), (-1, 0), (0, 1)]


def genlab(width, height, fillpersent):
    Map = []
    for i in range(height):
        g = []
        for j in range(width):
            g.append(0)
        Map.append(g)
    newtons = [(random.randint(1, height - 2), random.randint(1, width - 2))]
    Map[newtons[0][0]][newtons[0][1]] = 1
    tons = newtons.copy()

    s = width * height
    while len(tons) / s < fillpersent / 100:
        while newtons:
            newnewtons = []
            for i in range(len(newtons)):
                m = []
                for k in range(len(costil)):
                    if Map[newtons[i][0] + costil[k][0]][newtons[i][1] + costil[k][1]] == 0:
                        m.append(k)
                h = 0
                while m:
                    a = random.randint(0, len(m) - 1)
                    if random.randint(0, 100) == 1 or (len(m) == 1 and h == 0):
                        b = newtons[i][0] + costil[m[a]][0]
                        c = newtons[i][1] + costil[m[a]][1]
                        if b > 0 and b < height - 1 and c > 0 and c < width - 1:
                            f = []
                            for k in range(len(costil)):
                                if Map[b + costil[k][0]][c + costil[k][1]] == 1:
                                    f.append(k)
                            if len(f) == 1:
                                Map[b][c] = 1
                                newnewtons.append((b, c))
                                h += 1
                            elif len(f) == 2:
                                d = abs(f[0] - f[1])
                                if d == 2:
                                    Map[b][c] = 1
                                    newnewtons.append((b, c))
                                    h += 1
                                else:
                                    if Map[b + costil[f[0]][0] + costil[f[1]][0]][
                                        c + costil[f[0]][1] + costil[f[1]][1]] == 0:
                                        Map[b][c] = 1
                                        newnewtons.append((b, c))
                                        h += 1

                    m.pop(a)
            for i in range(len(newtons)):
                if not newtons[i] in tons:
                    tons.append(newtons[i])
            newtons = newnewtons
        newtons = [tons[random.randint(0, len(tons) - 1)]]
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
    a = False
    for i in range(height - 1, 0, -1):
        for j in range(width - 1, 0, -1):
            if Map[i][j] == 1:
                Map[i][j] = 3
                a = True
                break
        if a:
            break

    return Map, pos


graf = {0: "@", 1: "_", 2: "b", 3: "w"}


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
    rot = 0
    print("""Ты - крот, который немножко заблудился. Твоя задача - 
на ощупь найти выход из подземных тунелей. 
Ты можешь: двигаться вперед командой - 'w' и поворачивать вправо и 
влево на 90 градусов командами 'r' и 'l' соответственно.
Удачи в поисках выхода.""")
    while lab[pos[0]][pos[1]] != 3:
        a = input()
        if a == "w":
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Впереди стена")
            else:
                print("Ты продвинулся")
                pos[0] += costil[rot][0]
                pos[1] += costil[rot][1]
        if a == "r":
            rot += 1
            if rot == 4: rot = 0
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Ты повернулся вправо, впереди стена")
            else:
                print("Ты повернулся вправо, впереди нет стены")
        if a == "l":
            rot -= 1
            if rot == -1: rot = 3
            if lab[pos[0] + costil[rot][0]][pos[1] + costil[rot][1]] == 0:
                print("Ты повернулся влево, впереди стена")
            else:
                print("Ты повернулся влево, впереди нет стены")
    print("Ты ПАБЕДИЛ!!!")

