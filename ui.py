import pygame, sys, math
from pygame.locals import *
from math import tan, radians

TRIANGLE_EDGE = 50
TRIANGLE_HEIGHT = TRIANGLE_EDGE / 2 * math.tan((math.radians(60)))

DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800

OFFSET = 20

class Triangle(object):
    def __init__(self):
        self.visible = False
        self.hover = False
        self.touch = False
        self.middle_number = None

    def draw(self, display_surface):
        if not self.visible and not self.hover:
            return

        color = (0, 0, 0)
        width = 1

        if self.touch:
            color = (255, 127, 127)
            width = 0
        elif self.hover:
            width = 3

        pygame.draw.polygon(display_surface, color, self.get_coordinates(), width)


class DownTriangle(Triangle):
    def __init__(self, top_left_corner):
        super(self.__class__, self).__init__()
        self.top_left_corner = top_left_corner
        self.top_right_corner = (top_left_corner[0] + TRIANGLE_EDGE, top_left_corner[1])
        self.bottom_corner = (top_left_corner[0] + TRIANGLE_EDGE / 2, top_left_corner[1] + TRIANGLE_HEIGHT)
        self.numbers = {}

    def get_coordinates(self):
        return self.top_left_corner, self.top_right_corner, self.bottom_corner

    def point_is_in(self, point):
        left_slope = (self.bottom_corner[1] - self.top_left_corner[1]) / (self.bottom_corner[0] - self.top_left_corner[0])
        y_projection_on_left_line = left_slope * point[0] + self.top_left_corner[1] - left_slope * self.top_left_corner[0]

        right_slope = (self.top_right_corner[1] - self.bottom_corner[1]) / (self.top_right_corner[0] - self.bottom_corner[0])
        y_projection_on_right_line = right_slope * point[0] + self.top_right_corner[1] - right_slope * self.top_right_corner[0]

        return y_projection_on_left_line >= point[1] and y_projection_on_right_line >= point[1] >= self.top_left_corner[1]


class UpTriangle(Triangle):
    def __init__(self, top):
        super(self.__class__, self).__init__()
        self.top_corner = top
        self.bottom_left_corner = (top[0] - TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
        self.bottom_right_corner = (top[0] + TRIANGLE_EDGE / 2, top[1] + TRIANGLE_HEIGHT)
        self.numbers = {}

    def get_coordinates(self):
        return self.top_corner, self.bottom_right_corner, self.bottom_left_corner

    def point_is_in(self, point):
        left_slope = (self.top_corner[1] - self.bottom_left_corner[1]) / (self.top_corner[0] - self.bottom_left_corner[0])
        y_projection_on_left_line = left_slope * point[0] + self.top_corner[1] - left_slope * self.top_corner[0]

        right_slope = (self.bottom_right_corner[1] - self.top_corner[1]) / (self.bottom_right_corner[0] - self.top_corner[0])
        y_projection_on_right_line = right_slope * point[0] + self.top_corner[1] - right_slope * self.top_corner[0]

        return y_projection_on_left_line <= point[1] and y_projection_on_right_line <= point[1] <= self.bottom_left_corner[1]


def determine_where(position):
    x = int((position[0] - OFFSET) / TRIANGLE_EDGE)
    y = int((position[1] - OFFSET) / TRIANGLE_HEIGHT)
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
            triangle.draw(DISPLAYSURF)


pygame.init()
DISPLAYSURF = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))
DISPLAYSURF.fill((255, 255, 255))

pygame.display.set_caption('Hello World!')

cursor = (OFFSET, OFFSET)

triangle_columns = int((DISPLAY_WIDTH / TRIANGLE_EDGE) - 1) * 2
triangle_rows = int((DISPLAY_HEIGHT / TRIANGLE_HEIGHT) - 1)

triangles = []
previous_hover = None
previous_touch = None

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


def quit():
    pygame.quit()
    sys.exit()


def mouse_motion(event):
    global previous_hover
    triangle_at_position = get_triangle_at(event.pos)
    
    if previous_hover is not None:
        previous_hover.hover = False
    if triangle_at_position is not None:
        triangle_at_position.hover = True
    previous_hover = triangle_at_position


def mouse_down(event):
    global previous_touch
    triangle_at_position = get_triangle_at(event.pos)

    if previous_touch is not None and previous_touch != triangle_at_position:
        previous_touch.touch = False
    if triangle_at_position is not None:
        triangle_at_position.touch = not triangle_at_position.touch
        triangle_at_position.visible = not triangle_at_position.visible
        previous_touch = triangle_at_position


while True:  # main game loop
    DISPLAYSURF.fill((255, 255, 255))
    draw_triangles()

    for event in pygame.event.get():
        if event.type == pygame.locals.QUIT:
            quit()
        elif event.type == pygame.locals.MOUSEMOTION:
            mouse_motion(event)
        elif event.type == pygame.locals.MOUSEBUTTONDOWN:
            mouse_down(event)

    pygame.display.update()

