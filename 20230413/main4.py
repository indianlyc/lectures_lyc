import pygame
import random
import numpy as np

WIDTH = 360
HEIGHT = 480
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

r = 10

x, y = (WIDTH-r//2)//2 + 100, (HEIGHT-r//2)//2
g = 10
dt = 0.1
vy = 0


def draw_lines(surface: pygame.surface.Surface, color: pygame.color.Color, xs: list[int], ys: list[int]) -> None:
    """
    Рисуем параболу с помощью pyGame
    :param surface:
    :param color:
    :param xs:
    :param ys:
    :return: None
    """
    # print(xs[:3])
    # print(ys[:3])
    x1 = xs[0]
    y1 = ys[0]
    for i in range(1, len(xs)):
        x2 = xs[i]
        y2 = ys[i]
        pygame.draw.line(surface, color, (x1, y1), (x2, y2))
        # print(x1,y1, x2, y2)
        x1, y1 = x2, y2


x_parable = np.arange(0, WIDTH+1, 1)


def f_parabble(x, xs):
    m = max((xs - WIDTH//2)**2)
    (x - WIDTH//2)**2
    return HEIGHT - (((x - WIDTH//2)**2)/m*HEIGHT).astype(int)

def pf_parabble(x, xs):
    m = max((xs - WIDTH//2)**2)
    return HEIGHT - (((x - WIDTH//2)**2)/m*HEIGHT).astype(int)


y_parable = f_parabble(x_parable, x_parable)
# print(x_parable)
# print(y_parable)
# Создаем игру и окно
pygame.init()
# pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()
# Цикл игры
running = True
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверяем хотят ли выйти
        if event.type == pygame.QUIT:
            running = False

    # a = dv / dt -> dv = a * dt
    vy = vy + g * dt
    # v = dy  / dt -> dy = v * dt
    y = y + vy * dt

    if y > HEIGHT:
        y = HEIGHT
        vy = -vy

    if f_parabble(np.array([x]), x_parable)[0] < y:
        y = f_parabble(np.array([x]), x_parable)[0]
        vy = -vy

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, [x, y], r)
    draw_lines(screen, GREEN, x_parable, y_parable)
    pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    pass