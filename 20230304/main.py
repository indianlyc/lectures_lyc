import pygame
import random

W, H = 800, 600  # ширина и высота окна
FPS = 30  # количестко обработок в секунду (кадров)
count_rock = 3 # количество камней

# цвета в rgb
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (120, 120, 120)


x0, y0 = W//2, H//2  # начальные положение головы змеи
x0_change, y0_change = 0, 0  # начальные сдвиг змеи
snake_block = 10  # ширина змеи


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
        pygame.draw.rect(screen, RED, (el[0], el[1], snake_block, snake_block))


def draw_rock(rock_list):
    """
    Отрисовка камней
    :param snake_list:
    :return:
    """
    for el in rock_list:  # идем по всем элементам змеи
        # и рисуем прямоугольники на месте элементов
        pygame.draw.rect(screen, GRAY, (el[0], el[1], snake_block, snake_block))


def generate_food():
    """
    Генерируем координаты еды
    :return:
    """
    x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block
    return x, y

def generate_rock():
    """
    Генерируем координаты еды
    :return:
    """
    x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block
    return x, y


if __name__ == "__main__":
    pygame.init()  # инициализируем модуль pygame

    running = True  # истина пока продолжается игра
    game_over = False  # проиграли или нет
    screen = pygame.display.set_mode((W, H))  # получаем объект cодержимого окна с ширной W и высотой H

    pygame.display.set_caption("Игра Змейка")  # устанавливаем у окна заголовок
    clock = pygame.time.Clock()  # получаем объект "часы"
    font_style = pygame.font.SysFont(None, 50)  # получаем объект стиль-текста

    foodx, foody = generate_food()  # генерируем начальное положение еды
    rock_list = []  # список камней
    for i in range(count_rock):
        rock_list.append(generate_rock())

    snake_list = []  # список частей змейки
    length_snake = 1  # какой длинны должна быть змейка

    while running:  # основной цикл игры
        # получаем все события, зарегистрированные в игре
        for event in pygame.event.get():
            # если пользователь нажал крестик на окне
            if event.type == pygame.QUIT:
                # прерываем основной цикл (чтобы закрыть потом приложение)
                running = False
            # если регистрируем событие нажатой клавиши
            elif event.type == pygame.KEYDOWN:
                # если нажата клавиша стрелочка влево
                if event.key == pygame.K_LEFT:
                    # обновляем значения на сколько и куда надо сместить голову змеи
                    x0_change = -snake_block
                    y0_change = 0
                elif event.key == pygame.K_RIGHT:
                    x0_change = snake_block
                    y0_change = 0
                elif event.key == pygame.K_UP:
                    x0_change = 0
                    y0_change = -snake_block
                elif event.key == pygame.K_DOWN:
                    x0_change = 0
                    y0_change = snake_block
        # вычислили куда надо сместиться теперь смещаем
        # и запоминаем где должна быть голова змеи
        # обратите внимание, что если пользователь ничего не нажимает
        # то значение смещений остается и змея продолжает двигаться
        # в сторону последнего заданного направления
        x0 += x0_change
        y0 += y0_change

        # добавляем новый элемент змеи в конец списка
        snake_list.append((x0, y0))

        # если длинна списка элементов больше чем должно быть у змеи
        if len(snake_list) > length_snake:
            # удаляем первый элемент списка (хвост змеи)
            snake_list.pop(0)

        # если змея столкнулась сама с собой
        for el in snake_list[:-1]:
            if el == snake_list[-1]:
                # то игра заканчивается
                game_over = True

        # если змея вышла за границы поля
        if x0 > W or x0 < 0 or y0 > H or y0 < 0:
            # то игра заканчивается
            game_over = True

        # если змея столкнулась со скалами
        if (x0, y0) in rock_list:
            game_over = True

        # заполняем область окна белым цветом
        screen.fill(WHITE)

        # если игра закончилась
        if game_over:
            # рисуем в цетре экрана - вы проиграли
            message("Вы проиграли", GREEN)

        # выводим сколько съели
        message_count_eat(f"Съели: {length_snake-1}")

        # рисуем змею в текущих координатах ее частей
        draw_snake(snake_list)
        # рисуем еду
        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])
        # рисуем камни
        draw_rock(rock_list)

        # отображаем на экране то, что нарисовали
        pygame.display.update()

        # если голова змеи оказалась в той же клетке, что еда
        if (x0, y0) == (foodx, foody):
            # генерируем новую позицию еды
            foodx, foody = generate_food()
            # увеличиваем должную длинну змеи на 1
            length_snake += 1

        # если выполнили все слишком быстро ждем пока закончится время одного тика
        clock.tick(FPS)

    # если вышли из основного цикла
    # закрываем pygame
    pygame.quit()
    # закрываем python программу
    quit()
