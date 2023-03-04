import random
import pygame
import logging

logging.basicConfig(level=logging.INFO, filename="snake.log",filemode="w",
                    format="%(asctime)s %(filename)s %(levelname)s %(funcName)s %(lineno)d %(message)s")


W, H = 800, 600  # ширина и высота окна
FPS = 20  # количество обработок в секунду (кадров)
count_rock = 10 # количество камней
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


def draw_food(food):
    pygame.draw.rect(screen, GREEN, (food.x, food.y, snake_block, snake_block))


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

    def __repr__(self):
        return f"({self.x},{self.y})"


class Game:
    def __init__(self):
        self.power = 100
        self.game_over = False  # проиграли или нет
        # начальные положение головы змеи
        self.head = Point(W // 2, H // 2)
        # начальные сдвиг змеи
        self.head_change = Point(0, 0)
        # предыдущий сдвиг змеи
        self.head_change_old = Point(0, 0)
        # генерируем начальное положение еды
        self.new_food()
        # список камней
        self.rock_list = self.generate_rock()
        # список частей змейки
        self.snake_list = []
        # какой длинны должна быть змейка
        self.length_snake = 1

    def get_random_coordinate(self, max_l):
        return round(random.randrange(0, max_l - snake_block) / snake_block) * snake_block

    def get_random_place(self, max_w=W, max_h=H):
        return Point(self.get_random_coordinate(max_w), self.get_random_coordinate(max_h))

    def generate_rock(self):
        """
        Генерируем координаты еды
        """
        a = []
        for i in range(count_rock):
            a.append(self.get_random_place())
        return a

    def new_food(self):
        self.food = self.get_random_place()

    def snake_eat(self):
        # если мы еще в игре
        # и если голова змеи оказалась в той же клетке, что еда
        if not self.game_over and self.head == self.food:
            self.power += 100
            # генерируем новую позицию еды
            self.new_food()
            # увеличиваем должную длинну змеи на 1
            self.length_snake += 1

    def snake_hit_itself(self):
        for el in self.snake_list[:-1]:
            if el == self.snake_list[-1]:
                # то игра заканчивается
                self.game_over = True

    def snake_left_field(self):
        # если змея вышла за границы поля
        if self.head.x >= W or self.head.x < 0 or self.head.y >= H or self.head.y < 0:
            # то игра заканчивается
            self.game_over = True

    def snake_hit_rock(self):
        # если змея столкнулась со скалами
        if self.head in self.rock_list:
            self.game_over = True

    def snake_step(self):
        # вычислили куда надо сместиться теперь смещаем
        # и запоминаем где должна быть голова змеи
        # обратите внимание, что если пользователь ничего не нажимает
        # то значение смещений остается и змея продолжает двигаться
        # в сторону последнего заданного направления
        if not self.game_over:
            if self.length_snake > 1:
                if self.head_change == -self.head_change_old:
                    self.head_change = self.head_change_old

            self.head += self.head_change

            # добавляем новый элемент змеи в конец списка
            self.snake_list.append(game.head)

            # если длинна списка элементов больше чем должно быть у змеи
            if len(self.snake_list) > self.length_snake:
                # удаляем первый элемент списка (хвост змеи)
                self.snake_list.pop(0)
        logging.info(f"{self.snake_list}")

    def snake_left(self):
        self.power -= 1
        self.head_change = Point(-snake_block, 0)

    def snake_right(self):
        self.power -= 1
        self.head_change = Point(snake_block, 0)

    def snake_up(self):
        self.power -= 1
        self.head_change = Point(0, -snake_block)

    def snake_down(self):
        self.power -= 1
        self.head_change = Point(0, snake_block)

    def last_do(self):
        self.head_change_old = self.head_change


def do(game):
    pass



if __name__ == "__main__":
    logging.info(f"{W=} {H=} {count_rock=} {FPS + 100=} {snake_block=}")
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
        do(game)
                # # если нажата клавиша стрелочка влево
                # elif event.key == pygame.K_LEFT:
                #     # обновляем значения на сколько и куда надо сместить голову змеи
                #     game.snake_left()
                # elif event.key == pygame.K_RIGHT:
                #     game.snake_right()
                # elif event.key == pygame.K_UP:
                #     game.snake_up()
                # elif event.key == pygame.K_DOWN:
                #     game.snake_down()

        # логика действий перед отрисовкой ------
        # шагаем змеей
        game.snake_step()
        # змея столкнулась сама с собой?
        game.snake_hit_itself()
        # змея вышла за границы поля?
        game.snake_left_field()
        # если змея столкнулась со скалами
        game.snake_hit_rock()
        # ---------------------------------------

        # начало рисования --------------------------------
        # заполняем область окна белым цветом
        screen.fill(WHITE)

        # рисуем змею в текущих координатах ее частей
        draw_snake(game.snake_list)
        # рисуем еду
        draw_food(game.food)
        # рисуем камни
        draw_rock(game.rock_list)

        # если игра закончилась
        if game.game_over:
            # рисуем в цетре экрана - вы проиграли
            message("Вы проиграли", GREEN)

        # выводим сколько съели
        message_count_eat(f"Съели: {game.length_snake - 1}")
        # конец рисования ---------------------------------------

        # отображаем на экране то, что нарисовали
        pygame.display.update()

        # логика действий после отрисовки (подготовка к следующей итерации цикла) ------------
        # пробуем змеей съесть еду (если вдруг на ней находимся)
        game.snake_eat()
        game.last_do()
        # ------------------------------------------------------------------------------------

        # если выполнили все слишком быстро ждем пока закончится время одного тика
        clock.tick(FPS)

    # если вышли из основного цикла
    # закрываем pygame
    pygame.quit()
    # закрываем python программу
    quit()
