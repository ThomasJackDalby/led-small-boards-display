# game_of_life.py

import math
import random
import time
from led_display import LedDisplay

WHITE = (5, 5, 5)
BLACK = (0, 0, 0)
DATA = [None, None]

# populate initial data randomly
for i in range(2):
    DATA[i] = [None for _ in range(0, 9*8)]
    for y in range(0, 8):
        DATA[i][y] = [random.random() > 0.7 for _ in range(0, 9*8)]

display = LedDisplay(machine.Pin.board.GP28, boards=9)

index = 0
while True:
    next_index = (index + 1) % 2

    for y in range(0, 8):
        for x in range(0, display.total_columns):      
            alive = 0

            for dx in [-1, 0, 1]:
                tx = x + dx
                if tx < 0 or tx >= display.total_columns: continue

                for dy in [-1, 0, 1]:
                    ty = y + dy
                    if dx == 0 and dy == 0: continue
                    if ty < 0 or ty >= display.total_rows: continue           
                    if DATA[index][ty][tx]: alive += 1

            if DATA[index][y][x]:
                if alive < 2 or alive > 3: result = False
                else: result = True
                display.set_pixel(x, y, WHITE)
            else:
                if alive == 3: result = True
                else: result = False
                display.set_pixel(x, y, BLACK)
            DATA[next_index][y][x] = result
    index = (index + 1) % 2
    display.write()