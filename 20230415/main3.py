import pygame
import random
import numpy as np

WIDTH = 500
HEIGHT = 500
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

r = 5
g = 10
dt = 1

n = 100000
xs = np.random.random((n,)) * WIDTH
ys = np.random.random((n,)) * HEIGHT
vys = np.random.random((n,))
vxs = np.random.random((n,))


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

    xs = xs + vxs * dt
    ys = ys + vys * dt

    vxs[xs < 0] = np.abs(vxs[xs < 0])
    vys[ys < 0] = np.abs(vys[ys < 0])
    vxs[xs > WIDTH] = -np.abs(vxs[xs > WIDTH])
    vys[ys > HEIGHT] = -np.abs(vys[ys > HEIGHT])

    print((np.mean(np.sqrt(vxs**2 + vys**2)))**2)

    screen.fill(BLACK)
    for i in range(xs.shape[0]):
        pygame.draw.circle(screen, RED, [xs[i], ys[i]], r)
    pygame.display.flip()

pygame.quit()


if __name__ == "__main__":
    pass