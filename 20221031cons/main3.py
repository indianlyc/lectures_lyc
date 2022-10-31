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
    # как видно из этой функции мы не весь парсинг перенесли в функцию parse_argv
    # сделаем это в следующей итерации
    i1 = sys.argv.index("--add")
    i2 = sys.argv.index("--dt")
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
    # вынесли задачу парсинга аргументов в отдельную функцию
    if "--add" in argv:
        return "add"
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

    # Может показаться, что мы проделали одну и ту же работу дважды: выбор функции в зависимости от параметров,
    # но это не совсем так. Мы отвязали вид аргументов командной строки, от внутренней логики программы.
    # Теперь, если мы захотим, чтобы, например, удаление задачи было, не по параметру --del, а по параметру --remove
    # нам надо будет это изменить только в одном месте - в функции парсинга параметров
    # мы даже можем оставить оба варианта  (для удобства пользователей)
    # и --del и --remove, чтобы они означали одно и тоже - удаление задачи.


