import pygame, sys, math
from pygame.locals import *

TRIANGLE_EDGE = 75
TRIANGLE_HEIGHT = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

OFFSET = 20;


class Triangle:
    def __init__(self, faces_down, position):
        self.visible = False
        self.position = position
        self.faces_down = faces_down
        self.numbers = {}

    def draw(self):
        if self.faces_down:
            self.draw_down_triangle()
        else:
            self.draw_up_triangle()

    def draw_up_triangle(self, color=(0, 0, 0)):
        bottom_left = (self.position[0] - TRIANGLE_EDGE / 2, self.position[1] + TRIANGLE_HEIGHT)
        bottom_right = (self.position[0] + TRIANGLE_EDGE / 2, self.position[1] + TRIANGLE_HEIGHT)
        pygame.draw.polygon(DISPLAYSURF, color, (bottom_left, bottom_right, self.position), 1)

    def draw_down_triangle(self, color=(0, 0, 0)):
        height = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))
        top_right = (self.position[0] + TRIANGLE_EDGE, self.position[1])
        bottom = (self.position[0] + TRIANGLE_EDGE / 2, self.position[1] + height)

        pygame.draw.polygon(DISPLAYSURF, color, (bottom, self.position, top_right), 1)


def determine_where(position):
    x = int((position[0] - OFFSET) / TRIANGLE_EDGE)
    y = int((position[1] - OFFSET) / TRIANGLE_HEIGHT)
    print '{0}, {1}'.format(x, y)


pygame.init()
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
DISPLAYSURF.fill((255, 255, 255))

pygame.display.set_caption('Hello World!')

cursor = (OFFSET, OFFSET)

triangle_columns = int((DISPLAY_WIDTH / TRIANGLE_EDGE) - 1) * 2
triangle_rows = int((DISPLAY_HEIGHT / TRIANGLE_HEIGHT) - 1)

triangles = []

row_start_down = True
for row in range(0, triangle_rows):
    down = row_start_down
    row_list = []
    
    for column in range(0, triangle_columns):
        row_list.append(Triangle(down, cursor))

        if down:
            cursor = (cursor[0] + TRIANGLE_EDGE, cursor[1])

        row_list[column].draw()
        down = not down

    triangles.append(row_list)

    row_start_down = not row_start_down
    if not row_start_down:
        cursor = (OFFSET + TRIANGLE_EDGE / 2, cursor[1] + TRIANGLE_HEIGHT)
    else:
        cursor = (OFFSET, cursor[1] + TRIANGLE_HEIGHT)

while True:  # main game loop
    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            determine_where(event.pos)
    pygame.display.update()
