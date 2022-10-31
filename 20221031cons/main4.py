import sys

"""_summary_
Запоминаем задачи в файл

Использование:
Добавить задачу
python main.py --add Поучаствовать в олимпиаде --dt 2022-11-02T14:00:00 --label олимпиада
Список задач
python main.py --list
Удалить задачу
python main.py --del олимпиада
"""

"""
0. Код линеен, с сильной взаимозависимостью скорее всего его сложно будет изменять. 
Отсюда нобходиомсть делить код на части. 
Вынесли функции
"""


def add_f():
    with open(filename, "a") as f:
        f.write(" ".join(sys.argv[i1 + 1:i2]) + "," + sys.argv[i2 + 1] + "," + sys.argv[i2 + 3] + "\n")


def del_f():
    all_tasks = []
    with open(filename) as f:
        for line in f.readlines():
            all_tasks.append(line)

    with open(filename, "w") as f:
        for task in all_tasks:
            if "," in task:
                describe, dt, label = task.split(",")
                if label.strip() != sys.argv[2].strip():
                    f.write(task)


def list_f():
    with open(filename) as f:
        for line in f.readlines():
            print(line, end="")


def parse_argv(argv):
    if "--add" in argv:
        i1 = argv.index("--add")
        i2 = argv.index("--dt")
        return "add", i1, i2  # столкнулись с проблемой, что функция может возвращать разное число параметров
    # обычно это решается с помощью введения новой структуры данных
    # описывающей вывод
    elif "--list" in argv:
        return "list"
    elif "--del" in argv:
        return "del"


if __name__ == "__main__":
    # print(sys.argv)
    filename = "todo.txt"
    param = parse_argv(sys.argv)

    if param == "add":
        add_f()
    elif param == "del":
        del_f()
    elif param == "list":
        list_f()



