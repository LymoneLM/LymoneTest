import pygame
import random

# 初始化pygame
pygame.init()

# 游戏窗口大小
WIDTH, HEIGHT = 640, 480
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("贪吃蛇游戏")

# 颜色定义
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# 蛇的方块大小和初始速度
SNAKE_BLOCK = 10
SNAKE_SPEED = 15

# 定义蛇的初始位置和身体列表
snake_position = [100, 50]
snake_body = [[100, 50], [90, 50], [80, 50]]
# 初始方向
direction = "RIGHT"

# 食物位置
food_position = [random.randrange(1, (WIDTH // SNAKE_BLOCK)) * SNAKE_BLOCK,
                 random.randrange(1, (HEIGHT // SNAKE_BLOCK)) * SNAKE_BLOCK]
food_spawn = True

# 游戏结束标志
game_over = False

# 游戏主循环的时钟
clock = pygame.time.Clock()


def draw_snake(snake_body):
    """绘制蛇的函数"""
    for pos in snake_body:
        pygame.draw.rect(win, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_BLOCK, SNAKE_BLOCK))


def message(msg, color):
    """在屏幕上显示消息的函数"""
    font_style = pygame.font.SysFont(None, 30)
    mesg = font_style.render(msg, True, color)
    win.blit(mesg, [WIDTH / 6, HEIGHT / 3])  # 修正为blit


while not game_over:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and direction != "DOWN":
                direction = "UP"
            elif event.key == pygame.K_DOWN and direction != "UP":
                direction = "DOWN"
            elif event.key == pygame.K_LEFT and direction != "RIGHT":
                direction = "LEFT"
            elif event.key == pygame.K_RIGHT and direction != "LEFT":
                direction = "RIGHT"

    # 根据方向移动蛇
    if direction == "UP":
        snake_position[1] -= SNAKE_BLOCK
    elif direction == "DOWN":
        snake_position[1] += SNAKE_BLOCK
    elif direction == "LEFT":
        snake_position[0] -= SNAKE_BLOCK
    elif direction == "RIGHT":
        snake_position[0] += SNAKE_BLOCK

    # 将新的头部位置插入到蛇身体前面
    snake_body.insert(0, list(snake_position))

    # 蛇头吃到食物
    if snake_position == food_position:
        food_spawn = False
        # 不需要弹出尾部，蛇身自然增长
    else:
        # 没吃到食物，弹出尾部（最后一个元素）
        snake_body.pop()

    # 重新生成食物
    if not food_spawn:
        food_position = [random.randrange(1, (WIDTH // SNAKE_BLOCK)) * SNAKE_BLOCK,
                         random.randrange(1, (HEIGHT // SNAKE_BLOCK)) * SNAKE_BLOCK]
        food_spawn = True

    # 绘制背景
    win.fill(BLACK)
    # 绘制食物
    pygame.draw.rect(win, RED, pygame.Rect(food_position[0], food_position[1], SNAKE_BLOCK, SNAKE_BLOCK))
    # 绘制蛇
    draw_snake(snake_body)

    # 检查游戏是否结束（撞墙或撞自己）
    if snake_position[0] < 0 or snake_position[0] >= WIDTH or snake_position[1] < 0 or snake_position[1] >= HEIGHT:
        game_over = True
    for block in snake_body[1:]:  # 跳过蛇头检查
        if snake_position == block:
            game_over = True

    pygame.display.update()
    clock.tick(SNAKE_SPEED)

# 游戏结束后的显示
win.fill(BLACK)
message("游戏结束", WHITE)
pygame.display.update()
pygame.time.wait(2000)
pygame.quit()