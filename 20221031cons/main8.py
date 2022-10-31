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
2. Классы позволяют объединять кода и данные относящиеся к одной подзадачи и тесно связанные друг с другом.
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


# Объединим параметры и функцию их обрабатывающую в одном классе
class Param:
    def __init__(self, argv):
        self.argv = argv
        self.command = None
        self.description = None
        self.datetime = None
        self.label = None

    def parse_argv(self):
        if "--add" in self.argv or "--append" in self.argv:
            i1 = self.argv.index("--add")
            i2 = self.argv.index("--dt")
            self.command = "add"
            self.description = " ".join(self.argv[i1 + 1:i2])
            self.datetime = self.argv[i2 + 1]
            self.label = self.argv[i2 + 3]
        elif "--list" in self.argv:
            self.command = "list"
        elif "--del" in self.argv or "--remove" in self.argv:
            self.command = "del"


if __name__ == "__main__":
    # print(sys.argv)
    filename = "todo.txt"

    # создаем объект параметров и передаем ему параметры
    param = Param(sys.argv)
    # вызываем функцию парсинга параметров
    # которая заполняет нужные параметры
    param.parse_argv()

    if param.command == "add":
        add_f(param)
    elif param.command == "del":
        del_f(param)
    elif param.command == "list":
        list_f(param)



