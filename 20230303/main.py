import pygame
import random

W, H = 800, 600
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)


x0, y0 = W//2, H//2
x0_change, y0_change = 0, 0
snake_block = 10


def message(msg, color):
    msg = font_style.render(msg, True, color)
    screen.blit(msg, (W//2 - msg.get_width()//2, H//2 - msg.get_height()//2))


def draw_snake(snake_list):
    for el in snake_list:
        pygame.draw.rect(screen, RED, (el[0], el[1], snake_block, snake_block))

def generate_food():
    x = round(random.randrange(0, W - snake_block) / snake_block) * snake_block
    y = round(random.randrange(0, H - snake_block)/snake_block) * snake_block
    return x, y


if __name__ == "__main__":
    pygame.init()

    running = True
    game_over = False
    screen = pygame.display.set_mode((W, H))
    pygame.display.set_caption("Игра Змейка")
    clock = pygame.time.Clock()
    font_style = pygame.font.SysFont(None, 50)

    foodx, foody = generate_food()

    snake_list = []
    length_snake = 1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
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
        x0 += x0_change
        y0 += y0_change

        snake_list.append((x0, y0))

        if len(snake_list) > length_snake:
            snake_list.pop(0)

        for el in snake_list[:-1]:
            if el == snake_list[-1]:
                game_over = True

        if x0 > W or x0 < 0 or y0 > H or y0 < 0:
            game_over = True

        screen.fill(WHITE)

        if game_over:
            message("Вы проиграли", GREEN)
        # pygame.draw.rect(screen, RED, [x0, y0, snake_block, snake_block])
        draw_snake(snake_list)
        pygame.draw.rect(screen, GREEN, [foodx, foody, snake_block, snake_block])

        pygame.display.update()


        if (x0, y0) == (foodx, foody):
            foodx, foody = generate_food()
            length_snake += 1

        clock.tick(FPS)


    pygame.quit()
    quit()
