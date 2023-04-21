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
dt = 0.0001
vy = 0
vx = 0


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
    return HEIGHT - (((x - WIDTH//2)**2)/m*HEIGHT).astype(int)


def pf_parabble(x, xs):
    m = max((xs - WIDTH//2)**2)
    return - 2 * HEIGHT/m * (x - WIDTH // 2)
    # y1 = f_parabble(x, xs)
    # y2 = f_parabble(x+1, xs)
    # return (y2 - y1)


E = (vx**2 + vy**2)/2 + g*(HEIGHT-y)

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
b = False
while running:
    # Держим цикл на правильной скорости
    clock.tick(FPS)
    # Ввод процесса (события)
    for event in pygame.event.get():
        # Проверяем хотят ли выйти
        if event.type == pygame.QUIT:
            running = False

    for i in range(1000):
        # a = dv / dt -> dv = a * dt
        vy = vy + g * dt
        # vx = vx

        # v = dy  / dt -> dy = v * dt
        y = y + vy * dt
        x = x + vx * dt
        if f_parabble(np.array([x]), x_parable)[0] < y:
            break

    # print("E", E)
    # print("x, y", x, y)
    # print("vx, vy", vx, vy)
    # new_E = (vx**2 + vy**2)/2 + g*(HEIGHT-y)
    # print("new_E", new_E)
    # deltaE = (new_E - E)/2
    # print("deltaE", deltaE)
    # y = y - deltaE/g
    # print("y", y)
    # vy = vy - np.sign(deltaE) * np.sqrt(np.abs(deltaE)*2 - vx**2)
    # print("vy", vy)

    print("b, x,y, v, h, E:", b, x, y, np.sqrt(vx**2 + vy**2), (HEIGHT-y), (vx**2 + vy**2)/2 + g*(HEIGHT-y))
    print("vx, vy", vx, vy)
    # if y > HEIGHT:
    #     y = HEIGHT
    #     vy = -vy

    if f_parabble(np.array([x]), x_parable)[0] < y and not b:
        b = True
        print("++++++")
        print("x, y", x,y)
        # print("old vx, vy", vx, vy)
        new_y = f_parabble(np.array([x]), x_parable)[0]
        y = new_y
        # module_v = np.sqrt(vx**2 + vy**2)
        # tg_v = np.array([vy]) / np.array([vx])
        # print("tg_v", tg_v)
        # new_module_v = module_v - np.sqrt((y - new_y)*g*2)
        # if tg_v < 1:
        #     vy = new_module_v  * tg_v
        #     vx = np.sqrt(new_module_v**2 - vy**2)
        # else:
        #     vx = new_module_v / tg_v
        #     vy = np.sqrt(new_module_v**2 - vx**2)
        # vx = vx[0]
        # vy = vy[0]
        # y = new_y
        # print("new vx, vy", vx, vy)
        # print("x, y", x,y)

        print("+++b x,y, v, h, E:", b, x, y, np.sqrt(vx**2 + vy**2), (HEIGHT-y), (vx**2 + vy**2)/2 + g*(HEIGHT-y))


        print("new y", y)
        tg_parabol = pf_parabble(np.array([x]), x_parable)[0]
        print("tg_parabol", tg_parabol)
        modul_v = np.sqrt(vx**2 + vy**2)
        print("modul_v", modul_v)
        tg_v = np.array([vy])/np.array([vx])
        print("tg_v", tg_v)
        print("угол наклона параболы", -np.arctan(tg_parabol), (-np.arctan(tg_parabol))*180/np.pi)
        print("угола наклона весктора скорости", np.arctan(tg_v), (np.arctan(tg_v))*180/np.pi)
        alpha_minus_beta = -np.arctan(tg_parabol) - (np.arctan(tg_v) + np.arctan(tg_parabol) )
        print("разность углов", alpha_minus_beta, alpha_minus_beta*180/np.pi)
        new_tan = np.tan(alpha_minus_beta)[0]
        print("new_tan", new_tan)
        print("--------")
        print("old vx, vy", vx, vy)
        if np.abs(new_tan) < 1:
            vy = np.sign(alpha_minus_beta[0]) * modul_v * new_tan
            print("vy", vy)
            vx = -(np.sign(alpha_minus_beta) * np.sqrt(modul_v**2 - vy**2))[0]
            print("new vx, vy", vx, vy)
        else:
            vx = -np.sign(alpha_minus_beta[0]) * modul_v/new_tan
            print("vx", vx)
            vy = (np.sign(alpha_minus_beta) * np.sqrt(modul_v**2 - vx**2))[0]
            print("new vx, vy", vx, vy)
        print("---b x,y, v, h, E:", b, x, y, np.sqrt(vx**2 + vy**2), (HEIGHT-y), (vx**2 + vy**2)/2 + g*(HEIGHT-y))
    else:
        b = False



    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, [x, y], r)
    draw_lines(screen, GREEN, x_parable, y_parable)
    pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    pass