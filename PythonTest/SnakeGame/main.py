import pygame
import random
import sys

pygame.init()

W, H = 640, 480
display = pygame.display.set_mode((W, H))
pygame.display.set_caption("贪吃蛇")

C_WHITE = (255, 255, 255)
C_GREEN = (0, 255, 0)
C_RED = (255, 0, 0)
C_BLACK = (0, 0, 0)

SIZE = 10
VEL = 15

s_pos = [100, 50]
s_body = [[100, 50], [90, 50], [80, 50]]
drc = "RIGHT"

f_pos = [random.randrange(1, (W // SIZE)) * SIZE,
         random.randrange(1, (H // SIZE)) * SIZE]
f_active = True

over = False

timer = pygame.time.Clock()


def draw_snake(body):
    for seg in body:
        pygame.draw.rect(display, C_GREEN, pygame.Rect(seg[0], seg[1], SIZE, SIZE))


def display_text(msg, color):
    try:
        font = pygame.font.SysFont("simhei", 30)
    except:
        font = pygame.font.SysFont(None, 30)
    text = font.render(msg, True, color)
    display.blit(text, (W / 6, H / 3))


while not over:
    for evt in pygame.event.get():
        if evt.type == pygame.QUIT:
            over = True
        elif evt.type == pygame.KEYDOWN:
            if evt.key == pygame.K_UP and drc != "DOWN":
                drc = "UP"
            elif evt.key == pygame.K_DOWN and drc != "UP":
                drc = "DOWN"
            elif evt.key == pygame.K_LEFT and drc != "RIGHT":
                drc = "LEFT"
            elif evt.key == pygame.K_RIGHT and drc != "LEFT":
                drc = "RIGHT"

    if drc == "UP":
        s_pos[1] -= SIZE
    elif drc == "DOWN":
        s_pos[1] += SIZE
    elif drc == "LEFT":
        s_pos[0] -= SIZE
    elif drc == "RIGHT":
        s_pos[0] += SIZE

    s_body.insert(0, list(s_pos))

    if s_pos == f_pos:
        f_active = False
    else:
        s_body.pop()

    if not f_active:
        f_pos = [random.randrange(1, (W // SIZE)) * SIZE,
                 random.randrange(1, (H // SIZE)) * SIZE]
        f_active = True

    display.fill(C_BLACK)
    pygame.draw.rect(display, C_RED, pygame.Rect(f_pos[0], f_pos[1], SIZE, SIZE))
    draw_snake(s_body)

    if s_pos[0] < 0 or s_pos[0] >= W or s_pos[1] < 0 or s_pos[1] >= H:
        over = True
    for seg in s_body[1:]:
        if s_pos == seg:
            over = True

    pygame.display.flip()
    timer.tick(VEL)

display.fill(C_BLACK)
display_text("游戏结束", C_WHITE)
pygame.display.update()
pygame.time.delay(2000)
pygame.quit()
sys.exit()