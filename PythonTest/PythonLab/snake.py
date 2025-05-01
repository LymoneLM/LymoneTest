import pygame
import random

# 游戏窗口尺寸
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600

# 蛇身和食物大小
BLOCK_SIZE = 20

# 颜色定义
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# 初始化 Pygame
pygame.init()

# 创建游戏窗口
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("贪吃蛇")

# 创建时钟对象，控制游戏帧率
clock = pygame.time.Clock()


class Snake:
    def __init__(self):
        self.head_pos = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        self.body = [self.head_pos]
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def move(self):
        if self.direction == "UP":
            self.head_pos[1] -= BLOCK_SIZE
        elif self.direction == "DOWN":
            self.head_pos[1] += BLOCK_SIZE
        elif self.direction == "LEFT":
            self.head_pos[0] -= BLOCK_SIZE
        elif self.direction == "RIGHT":
            self.head_pos[0] += BLOCK_SIZE

        # 更新整个蛇身体的位置
        self.body.insert(0, list(self.head_pos))
        if len(self.body) > score + 1:
            self.body.pop()

    def change_direction(self, direction):
        if direction == "UP" and self.direction != "DOWN":
            self.direction = "UP"
        elif direction == "DOWN" and self.direction != "UP":
            self.direction = "DOWN"
        elif direction == "LEFT" and self.direction != "RIGHT":
            self.direction = "LEFT"
        elif direction == "RIGHT" and self.direction != "LEFT":
            self.direction = "RIGHT"

    def grow(self):
        self.body.append(list(self.head_pos))

    def draw(self):
        for block in self.body:
            pygame.draw.rect(window, WHITE, (block[0], block[1], BLOCK_SIZE, BLOCK_SIZE))


class Food:
    def __init__(self):
        self.pos = [random.randrange(1, WINDOW_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(1, WINDOW_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

    def respawn(self):
        self.pos = [random.randrange(1, WINDOW_WIDTH // BLOCK_SIZE) * BLOCK_SIZE,
                    random.randrange(1, WINDOW_HEIGHT // BLOCK_SIZE) * BLOCK_SIZE]

    def draw(self):
        pygame.draw.rect(window, RED, (self.pos[0], self.pos[1], BLOCK_SIZE, BLOCK_SIZE))


# 创建蛇和食物对象
snake = Snake()
food = Food()

score = 0

game_over = False

# 游戏循环
while not game_over:
    # 处理事件
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.change_direction("UP")
            elif event.key == pygame.K_DOWN:
                snake.change_direction("DOWN")
            elif event.key == pygame.K_LEFT:
                snake.change_direction("LEFT")
            elif event.key == pygame.K_RIGHT:
                snake.change_direction("RIGHT")

    # 移动蛇
    snake.move()

    # 判断是否吃到食物
    if snake.head_pos == food.pos:
        snake.grow()
        food.respawn()
        score += 1

        # 更新蛇头位置
        snake.move()

    # 判断是否撞到墙壁或自身
    if (snake.head_pos[0] < 0 or snake.head_pos[0] >= WINDOW_WIDTH or
            snake.head_pos[1] < 0 or snake.head_pos[1] >= WINDOW_HEIGHT or
            snake.head_pos in snake.body[1:]):
        game_over = True

    # 绘制背景
    window.fill(BLACK)

    # 绘制蛇和食物
    snake.draw()
    food.draw()

    # 绘制分数
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    window.blit(score_text, (10, 10))

    # 刷新显示
    pygame.display.flip()

    # 控制游戏帧率
    clock.tick(10)

# 退出游戏
pygame.quit()