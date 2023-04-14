# Pygame шаблон - скелет для нового проекта Pygame
import pygame
import random

WIDTH = 360
HEIGHT = 480
FPS = 30
# Задаем цвета
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
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
            break

    screen.fill(BLACK)
    pygame.draw.circle(screen, RED, [(360-10)//2, (480-10)//2], 10)


    pygame.display.flip()

pygame.quit()



if __name__ == "__main__":
    pass