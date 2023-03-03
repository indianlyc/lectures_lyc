import pygame
import random

W, H = 800, 600  # ширина и высота окна
FPS = 30  # количество обработок в секунду (кадров)
count_rock = 3 # количество камней
snake_block = 10  # ширина змеи


# цвета в rgb
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (120, 120, 120)


def message(msg, color) -> None:
    """
    Вывод текста в центр экрана заданным цветом
    :param msg: текст
    :param color: цвет в rgb
    :return: None
    """
    msg = font_style.render(msg, True, color)  # преобразуем текст в изображение текста
    screen.blit(msg, (W//2 - msg.get_width()//2, H//2 - msg.get_height()//2))  # отображаем изображение на экране


def message_count_eat(msg) -> None:
    """
    Вывод текста в верхний левый угол экрана зеленым цветом
    :param msg: текст
    :return: None
    """
    msg = font_style.render(msg, True, GREEN)  # преобразуем текст в изображение текста
    screen.blit(msg, (0, 0))  # отображаем изображение на экране


def draw_snake(snake_list):
    """
    Отрисовка змеи
    :param snake_list:
    :return:
    """
    for el in snake_list:  # идем по всем элементам змеи
        # и рисуем прямоугольники на месте элементов
        pygame.draw.rect(screen, RED, (el.x, el.y, snake_block, snake_block))


def draw_rock(rock_list):
    """
    Отрисовка камней
    :param rock_list:
    :return:
    """
    for el in rock_list:  # идем по всем элементам змеи
        # и рисуем прямоугольники на месте элементов
        pygame.draw.rect(screen, GRAY, (el.x, el.y, snake_block, snake_block))


class Point:
    def __init__(self,  x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Point(self.x + other.x, self.y + other.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __neg__(self):
        return Point(-self.x, -self.y)


class Game:
    def __init__(self):
        self.game_over = False  # проиграли или нет
        # начальные положение головы змеи
        self.head = Point(W // 2, H // 2)
        # начальные сдвиг змеи
        self.head_change = Point(0, 0)
        # предыдущий сдвиг змеи
        self.head_change_old = Point(0, 0)
        # генерируем начальное положение еды
        self.food = self.generate_food()
        # список камней
        self.rock_list = self.generate_rock()
        # список частей змейки
        self.snake_list = []
        # какой длинны должна быть змейка
        self.length_snake = 1

    def generate_rock(self):
        """
        Генерируем координаты еды
        """
        a = []
        for i in range(count_rock):
            x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
            y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block
            a.append(Point(x, y))
        return a

    def generate_food(self):
        """
        Генерируем координаты еды
        :return:
        """
        x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
        y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block
        return Point(x, y)


if __name__ == "__main__":
    pygame.init()  # инициализируем модуль pygame

    screen = pygame.display.set_mode((W, H))  # получаем объект cодержимого окна с ширной W и высотой H
    pygame.display.set_caption("Игра Змейка")  # устанавливаем у окна заголовок
    clock = pygame.time.Clock()  # получаем объект "часы"
    font_style = pygame.font.SysFont(None, 50)  # получаем объект стиль-текста

    running = True  # истина пока продолжается игра
    game = Game()

    while running:  # основной цикл игры
        # получаем все события, зарегистрированные в игре
        for event in pygame.event.get():
            # если пользователь нажал крестик на окне
            if event.type == pygame.QUIT:
                # прерываем основной цикл (чтобы закрыть потом приложение)
                running = False
            # если регистрируем событие нажатой клавиши
            elif event.type == pygame.KEYDOWN:
                # если игра закончена и нажали c перезапускаем игру
                if game.game_over and event.key == pygame.K_c:
                    game = Game()
                # если нажата клавиша стрелочка влево
                elif event.key == pygame.K_LEFT:
                    # обновляем значения на сколько и куда надо сместить голову змеи
                    game.head_change = Point(-snake_block, 0)
                elif event.key == pygame.K_RIGHT:
                    game.head_change = Point(snake_block, 0)
                elif event.key == pygame.K_UP:
                    game.head_change = Point(0, -snake_block)
                elif event.key == pygame.K_DOWN:
                    game.head_change = Point(0, snake_block)

        # вычислили куда надо сместиться теперь смещаем
        # и запоминаем где должна быть голова змеи
        # обратите внимание, что если пользователь ничего не нажимает
        # то значение смещений остается и змея продолжает двигаться
        # в сторону последнего заданного направления
        if not game.game_over:
            if game.length_snake > 1:
                if game.head_change == -game.head_change_old:
                    game.head_change = game.head_change_old

            game.head += game.head_change

            # добавляем новый элемент змеи в конец списка
            game.snake_list.append(game.head)

            # если длинна списка элементов больше чем должно быть у змеи
            if len(game.snake_list) > game.length_snake:
                # удаляем первый элемент списка (хвост змеи)
                game.snake_list.pop(0)

        # если змея столкнулась сама с собой
        for el in game.snake_list[:-1]:
            if el == game.snake_list[-1]:
                # то игра заканчивается
                game.game_over = True

        # если змея вышла за границы поля
        if game.head.x >= W or game.head.x < 0 or game.head.y >= H or game.head.y < 0:
            # то игра заканчивается
            game.game_over = True

        # если змея столкнулась со скалами
        if game.head in game.rock_list:
            game.game_over = True

        # заполняем область окна белым цветом
        screen.fill(WHITE)

        # если игра закончилась
        if game.game_over:
            # рисуем в цетре экрана - вы проиграли
            message("Вы проиграли", GREEN)

        # выводим сколько съели
        message_count_eat(f"Съели: {game.length_snake-1}")

        # рисуем змею в текущих координатах ее частей
        draw_snake(game.snake_list)
        # рисуем еду
        pygame.draw.rect(screen, GREEN, (game.food.x, game.food.y, snake_block, snake_block))
        # рисуем камни
        draw_rock(game.rock_list)

        # отображаем на экране то, что нарисовали
        pygame.display.update()

        if not game.game_over:
            # если голова змеи оказалась в той же клетке, что еда
            if game.head == game.food:
                # генерируем новую позицию еды
                game.food = game.generate_food()
                # увеличиваем должную длинну змеи на 1
                game.length_snake += 1

        game.head_change_old = game.head_change
        # если выполнили все слишком быстро ждем пока закончится время одного тика
        clock.tick(FPS)

    # если вышли из основного цикла
    # закрываем pygame
    pygame.quit()
    # закрываем python программу
    quit()
