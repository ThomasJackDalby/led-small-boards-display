# matrix.py
# a matrix esk effect with lights trickling down the panels

import math
import random
import time
from led_display import LedDisplay

blobs = []
display = LedDisplay(machine.Pin.board.GP28, boards=9)

class Blob:
    def __init__(self, color, x, y):
        self.color = color
        self.x = x
        self.y = y

        self.colors = [color]
        for i in range(1, 10):
            self.colors.append(tuple(int(i*0.6) for i in self.colors[i-1]))
    
for i in range(200):
    y = random.randint(0, 7)
    x = random.randint(0, 8*9-1)

    c = (random.randint(0, 255),random.randint(0, 255),random.randint(0, 255))
    # c = (0,random.randint(0, 255),0)
    blob = Blob(c, x, y)
    for j, color in enumerate(blob.colors):
        display.set_pixel(blob.x-j, blob.y, color)

while True:
    display.pan_right()
    display.write()