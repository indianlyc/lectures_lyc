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
    with open(filename, "a") as f:
        f.write(param.description + "," + param.datetime + "," + param.label + "\n")


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
    def __init__(self, command, description=None, datetime=None, label=None):
        self.command = command
        self.description = description
        self.datetime = datetime
        self.label = label


def parse_argv(argv):
    if "--add" in argv or "--append" in argv:
        i1 = argv.index("--add")
        i2 = argv.index("--dt")
        # можно возвращать не индексы, а сразу осмысленные данные,
        # описывающие параметры задачи
        # description, datetime, label
        param = Param("add",
                      " ".join(argv[i1 + 1:i2]),  # description
                      argv[i2 + 1],  # datetime
                      argv[i2 + 3])   # label
    elif "--list" in argv:
        param = Param("list")
    elif "--del" in argv or "--remove" in argv:
        param = Param("del")
    return param

# Мы сейчас, имеет структуру данных Param и функцию parse_argv
# которые тесно связаны друг с другом. По сути функция заполняет свойства структуры
# Класс позволяет объединять данные и код относящиеся к одной подзадачи


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



