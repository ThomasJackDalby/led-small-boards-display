# snake.py
# unfinished snake.py clone

import math
import random
import time
from led_display import LedDisplay

RED = (255, 0, 0)

UP = 0
DOWN = 1
LEFT = 2
RIGHT = 3

DELTAS = [
    (0, 1),
    (0, -1),
    (-1, 0),
    (1, 0),
]

class Board:
    def __init__(self):
        self.width = 8 * 9
        self.height = 8
        self.food = []
        self.snakes = []

class Vector2D:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Snake:
    def __init__(self, x, y):
        self.head = Vector2D(x, y)
        self.body = []

    def update(self, board):
        directions = Directions(self, board)
        directions.avoid_walls()
        directions.avoid_self()
        directions.avoid_snakes()
        directions.move_towards_closest_food()
        direction = next(directions.get_directions())

        dx, dy = DELTAS[direction]
        self.body.insert(Vector2D(self.x, self.y))
        self.x += dx
        self.y += dy
        self.body.pop()

    def draw(self, display):
        pass

class Directions:

    def __init__(self, you, board):
        self.you = you
        self.board = board
        self.directions = [1,1,1,1]

    def avoid_walls(self):
        if self.you.head.x == 0: self.update(LEFT, 0)
        elif self.you.head.x == self.board.height - 1: self.update(RIGHT, 0)
        if self.you.head.y == 0: self.update(DOWN, 0)
        elif self.you.head.y == self.board.height - 1: self.update(UP, 0)

    def avoid_self(self):
        self.avoid_snake(self.you)

    def avoid_snakes(self):
        for snake in self.board.snakes:
            self.avoid_snake(snake)

    def avoid_snake(self, snake):
        head_x = self.you.head.x
        head_y = self.you.head.y

        for part in snake.body:
            if head_y == part.y:
                if head_x+1 == part.x: self.update(RIGHT, 0)
                elif head_x-1 == part.x: self.update(LEFT, 0)
            if head_x == part.x:
                if head_y+1 == part.y: self.update(UP, 0)
                elif head_y-1 == part.y: self.update(DOWN, 0)

    def move_towards_closest_food(self, factor=2):
        closest_food = get_closest_point_to(self.you.head, self.board.food)
        if closest_food is None: return None
        self.move_towards(closest_food, factor)

    def move_towards(self, point, factor):
        head_x = self.you.head.x
        head_y = self.you.head.y
        
        if point.y > head_y: self.update(UP, factor)
        elif point.y < head_y: self.update(DOWN, factor)
        if point.x < head_x:self.update(LEFT, factor)
        elif point.x > head_x: self.update(RIGHT, factor)

    def update(self, direction, factor):
        self.directions[direction] *= factor

    def get_directions(self):
        return (d for _, d in sorted(zip(self.directions, [0,1,2,3]), reverse=True))

def linear_distance(a, b):
    return abs(a.x - b.x) + abs(a.y - b.y)

def get_closest_point_to(source, targets):
    if len(targets) == 0: return None
    if len(targets) == 1: return targets[0]

    min_target = targets[0]
    min_distance = linear_distance(source, min_target)
    for target in targets[1:]:
        distance = linear_distance(source, target)
        if distance < min_distance:
            min_distance = distance
            min_target = target
    return min_target

def flood_fill(width, height, cells, sources):

    if len(cells) != width * height:
        raise Exception()

    counts = []
    queue = []
    groups = []
    for i, (x, y) in enumerate(sources):
        index = get_index(width, x, y)
        groups.append([i+1])
        queue.append(index)
        cells[index] = i+1
        counts.append(1)

    def flood(current_cell, next_x, next_y):
        if next_x < 0 or next_x >= width: return False
        if next_y < 0 or next_y >= height: return False
        next_cell = get_index(width, next_x, next_y)

        current_cell_value = cells[current_cell]
        next_cell_value = cells[next_cell]

        if next_cell_value == -1: return False
        elif next_cell_value == current_cell_value: return False
        elif next_cell_value == 0:
            cells[next_cell] = current_cell_value
            queue.append(next_cell)
            return True
        else:
            current_group = next(filter(lambda group: current_cell_value in group, groups))
            if cells[next_cell] in current_group: return False
            next_group = next(filter(lambda group: next_cell_value in group, groups))
            current_group.extend(next_group)
            groups.remove(next_group)
            return False

    while len(queue) > 0:
        current_cell = queue[0]
        queue = queue[1:]
        x, y = get_xy(width, current_cell)
        for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
            if flood(current_cell, x + dx, y + dy):
                yield cells
    
def get_index(width, x, y):
    return width * y + x

def get_xy(width, index):
    x = index % width
    y = (index - x) // width
    return x, y 

display = LedDisplay(machine.Pin.board.GP28, boards=9)

board = Board()
board.snakes.append(Snake(0, 0))

while True:
    # if random.random() > 0.9:
    #     x = random.randint(0, display.total_columns)
    #     y = random.randint(0, display.total_rows)
    #     board.food.append(Vector2D(x, y))

    for snake in board.snakes:
        snake.update(board)
        snake.draw(display)

    for x, y in board.food:
        display.set_pixel(x, y, RED)
    display.write()




