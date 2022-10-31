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
3. С помощью классов можно разделять внутреннюю логику и внешний интерфейс, внутренняя логика можно произвольным
образом меняться от версии класса (библиотеки классов) к версии, а внешний интерфейс при это оставаться
постоянным, для поддержки всех программистов которые используют эту библиотеку.
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


# Этот класс может писать программист1
class Param:
    def __init__(self, argv):
        # программисту1 задачи тз написать класс, который будет парсить командную строку,
        # и у которого будут свойства command, desription, datetime, label
        # для реализации этой задачи  ему понадобилась переменная  argv
        # и метод parse_argv, чтобы подчеркнуть что это не внешний интерфейс
        # а внутренние переменные он обозначил начало их имен нижним подчеркиванием
        # как это принято в Python
        self._argv = argv
        self.command = None
        self.description = None
        self.datetime = None
        self.label = None
        # вызов парсинга программист1 решил сделать прямо в функции __init__,
        # чтобы упростить жизнь программисту2, который будет пользоваться его классом
        self._parse_argv()

    def _parse_argv(self):
        if "--add" in self._argv or "--append" in self._argv:
            i1 = self._argv.index("--add")
            i2 = self._argv.index("--dt")
            self.command = "add"
            self.description = " ".join(self._argv[i1 + 1:i2])
            self.datetime = self._argv[i2 + 1]
            self.label = self._argv[i2 + 3]
        elif "--list" in self._argv:
            self.command = "list"
        elif "--del" in self._argv or "--remove" in self._argv:
            self.command = "del"


if __name__ == "__main__":
    # А эту часть кода уже может писать программист2
    # print(sys.argv)
    filename = "todo.txt"

    # и ему не надо знать никаких переменных или методов кроме те что помогают в решении его задачи
    param = Param(sys.argv)

    # оптимизируем выбор с помощью словаря
    d = {
        "add": add_f,
        "del": del_f,
        "list": list_f,
    }
    d[param.command](param)
