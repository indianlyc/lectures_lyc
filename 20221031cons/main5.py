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
Создали структуру данных для параметров
"""


def add_f(param):
    i1 = param["i1"]
    i2 = param["i2"]
    with open(filename, "a") as f:
        # оставшийся код зависимый от аргументов тоже надо перенести в функцию парсинга
        # сделаем это на следующих итерациях
        f.write(" ".join(sys.argv[i1 + 1:i2]) + "," + sys.argv[i2 + 1] + "," + sys.argv[i2 + 3] + "\n")


def del_f(param):
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


def list_f(param):
    with open(filename) as f:
        for line in f.readlines():
            print(line, end="")


# структура данных описывает необходимые данные после парсинга аргументов
param = {
    "command": None,
    "i1": None,
    "i2": None,
}


def parse_argv(argv):
    if "--add" in argv:
        param["i1"] = argv.index("--add")
        param["i2"] = argv.index("--dt")
        param["command"] = "add"
    elif "--list" in argv:
        param["command"] = "list"
    elif "--del" in argv:
        param["command"] = "del"
    return param


if __name__ == "__main__":
    # print(sys.argv)
    filename = "todo.txt"
    param = parse_argv(sys.argv)

    if param["command"] == "add":
        add_f(param)
    elif param["command"] == "del":
        del_f(param)
    elif param["command"] == "list":
        list_f(param)



