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

1. Классы могут быть использованы как собственные типы данных
"""


def add_f(param):
    i1 = param.i1
    i2 = param.i2
    with open(filename, "a") as f:
        # оставшийся код зависимый от аргументов тоже надо перенести в функцию парсинга
        # сделаем это на следующей итерации
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


# Вместо словаря воспользуемся классом
class Param:
    def __init__(self, command, i1=None, i2=None):
        self.command = command
        self.i1 = i1
        self.i2 = i2


def parse_argv(argv):
    if "--add" in argv:
        param = Param("add", argv.index("--add"), argv.index("--dt"))
    elif "--list" in argv:
        param = Param("list")
    elif "--del" in argv:
        param = Param("del")
    return param


if __name__ == "__main__":
    # print(sys.argv)
    filename = "todo.txt"
    param = parse_argv(sys.argv)

    if param.command == "add":
        add_f(param)
    elif param.command == "del":
        del_f(param)
    elif param.command == "list":
        list_f(param)



