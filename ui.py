import pygame, sys, math
from pygame.locals import *
from math import tan, radians

TRIANGLE_EDGE = 50
TRIANGLE_HEIGHT = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

OFFSET = 20

class DownTriangle:
    def __init__(self, top_left_corner):
        self.visible = False
        self.hover = False
        self.middle_number = None
        self.top_left_corner = top_left_corner
        self.top_right_corner = (top_left_corner[0] + TRIANGLE_EDGE, top_left_corner[1])
        self.bottom_corner = (top_left_corner[0] + TRIANGLE_EDGE / 2, top_left_corner[1] + TRIANGLE_HEIGHT)
        self.numbers = {}

    def draw(self):
        if not self.visible and not self.hover:
            return
        color = (0, 0, 0)
        width = 1

        if self.hover:
            width = 3

        pygame.draw.polygon(DISPLAYSURF, color, (self.top_left_corner, self.top_right_corner, self.bottom_corner), width)

    def point_is_in(self, point):
        left_slope = (self.bottom_corner[1] - self.top_left_corner[1]) / (self.bottom_corner[0] - self.top_left_corner[0])
        y_projection_on_left_line = left_slope * point[0] + self.top_left_corner[1] - left_slope * self.top_left_corner[0]

        right_slope = (self.top_right_corner[1] - self.bottom_corner[1]) / (self.top_right_corner[0] - self.bottom_corner[0])
        y_projection_on_right_line = right_slope * point[0] + self.top_right_corner[1] - right_slope * self.top_right_corner[0]

        return y_projection_on_left_line >= point[1] and y_projection_on_right_line >= point[1] and point[1] >= self.top_left_corner[1]


class UpTriangle:
    def __init__(self, top):
        self.visible = False
        self.hover = False
        self.middle_number = None
        self.top_corner = top
        self.bottom_left_corner = (top[0] - TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
        self.bottom_right_corner = (top[0] + TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
        self.numbers = {}

    def draw(self):
        if not self.visible and not self.hover:
            return

        color = (0, 0, 0)
        width = 1

        if self.hover:
            width = 3

        pygame.draw.polygon(DISPLAYSURF, color, (self.top_corner, self.bottom_right_corner, self.bottom_left_corner), width)

    def point_is_in(self, point):
        left_slope = (self.top_corner[1] - self.bottom_left_corner[1]) / (self.top_corner[0] - self.bottom_left_corner[0])
        y_projection_on_left_line = left_slope * point[0] + self.top_corner[1] - left_slope * self.top_corner[0]

        right_slope = (self.bottom_right_corner[1] - self.top_corner[1]) / (self.bottom_right_corner[0] - self.top_corner[0])
        y_projection_on_right_line = right_slope * point[0] + self.top_corner[1] - right_slope * self.top_corner[0]

        return y_projection_on_left_line <= point[1] and y_projection_on_right_line <= point[1] and point[1] <= self.bottom_left_corner[1]


def determine_where(position):
    x = int((position[0] - OFFSET) / TRIANGLE_EDGE)
    y = int((position[1] - OFFSET) / TRIANGLE_HEIGHT)
    print '{0}, {1}'.format(x, y)
    for row in triangles:
        for triangle in row:
            if triangle.point_is_in(position):
                triangle.touch = True


def get_triangle_at(position):
    for row in triangles:
        for triangle in row:
            if triangle.point_is_in(position):
                return triangle


def draw_triangles():
    for row in triangles:
        for triangle in row:
            triangle.draw()


pygame.init()
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
DISPLAYSURF.fill((255, 255, 255))

pygame.display.set_caption('Hello World!')

cursor = (OFFSET, OFFSET)

triangle_columns = int((DISPLAY_WIDTH / TRIANGLE_EDGE) - 1) * 2
triangle_rows = int((DISPLAY_HEIGHT / TRIANGLE_HEIGHT) - 1)

triangles = []
previous_hover = None

row_start_down = True
for row in range(0, triangle_rows):
    down = row_start_down
    row_list = []

    for column in range(0, triangle_columns):
        if down:
            row_list.append(DownTriangle(cursor))
            cursor = (cursor[0] + TRIANGLE_EDGE, cursor[1])
        else:
            row_list.append(UpTriangle(cursor))

        down = not down

    triangles.append(row_list)

    row_start_down = not row_start_down
    if not row_start_down:
        cursor = (OFFSET + TRIANGLE_EDGE / 2, cursor[1] + TRIANGLE_HEIGHT)
    else:
        cursor = (OFFSET, cursor[1] + TRIANGLE_HEIGHT)

while True:  # main game loop
    DISPLAYSURF.fill((255, 255, 255))
    draw_triangles()

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.locals.MOUSEMOTION:
            triangle_at_position = get_triangle_at(event.pos)
            if previous_hover != None:
                previous_hover.hover = False
            if triangle_at_position != None:
                triangle_at_position.hover = True

            previous_hover = triangle_at_position
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            triangle_at_position = get_triangle_at(event.pos)
            if triangle_at_position != None:
                triangle_at_position.visible = True
    pygame.display.update()

