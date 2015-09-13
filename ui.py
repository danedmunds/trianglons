import pygame, sys, math
from pygame.locals import *

TRIANGLE_EDGE = 75
TRIANGLE_HEIGHT = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800


def draw_up_triangle(top, color=(0, 0, 0)):
    bottom_left = (top[0] - TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
    bottom_right = (top[0] + TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
    pygame.draw.polygon(DISPLAYSURF, color, (bottom_left, bottom_right, top), 1)


def draw_down_triangle(top_left, color=(0, 0, 0)):
    height = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))
    top_right = (top_left[0] + TRIANGLE_EDGE, top_left[1])
    bottom = (top_left[0] + TRIANGLE_EDGE / 2, top_left[1] + height)

    pygame.draw.polygon(DISPLAYSURF, color, (bottom, top_left, top_right), 1)


pygame.init()
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
DISPLAYSURF.fill((255, 255, 255))

pygame.display.set_caption('Hello World!')

cursor = (20, 20)

down = True
for column in range(0, (int) ((DISPLAY_HEIGHT / TRIANGLE_HEIGHT) - 1)):
    for i in range(0, (int) ((DISPLAY_WIDTH / TRIANGLE_EDGE) - 1) * 2):
        if down:
            draw_down_triangle(cursor)
            cursor = (cursor[0] + TRIANGLE_EDGE, cursor[1])
        else:
            draw_up_triangle(cursor)
        down = not down

    if down:
        cursor = (20 + TRIANGLE_EDGE / 2, cursor[1] + TRIANGLE_HEIGHT)
    else:
        cursor = (20, cursor[1] + TRIANGLE_HEIGHT)
    down = not down

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        #        elif event.type == pygame.locals.MOUSEMOTION:
    pygame.display.update()
