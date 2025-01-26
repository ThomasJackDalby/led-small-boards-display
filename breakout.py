import math
import random
import time
from led_display import LedDisplay

display = LedDisplay(machine.Pin.board.GP28, boards=9)
VALUE = 50
scalar = float # a scale value (0.0 to 1.0)
def hsv_to_rgb(h:scalar, s:scalar, v:scalar) -> tuple:
    if s:
        if h == 1.0: h = 0.0
        i = int(h*6.0); f = h*6.0 - i
        
        w = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        if i==0: return (v, t, w)
        if i==1: return (q, v, w)
        if i==2: return (w, v, t)
        if i==3: return (w, q, v)
        if i==4: return (t, w, v)
        if i==5: return (v, w, q)
    else: 
        return (v, v, v)

class Ball:
    def __init__(self, x, y, vx, vy, hue):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        
        r, g, b = hsv_to_rgb(hue, 1, 1)
        self.color = (int(r*VALUE), int(g*VALUE), int(b*VALUE))

    def update(self, blocks):
        self.x = self.x+self.vx
        self.y = self.y+self.vy

        if self.x < 0:
            self.x = 0
            self.vx = -self.vx
        elif self.x >= 8*9:
            self.x = 8*9-1
            self.vx = -self.vx

        if self.y < 0:
            self.y = 0
            self.vy = -self.vy
        elif self.y >= 8:
            self.y = 7
            self.vy = -self.vy

        ball_xy = (int(self.x), int(self.y))
        if ball_xy in blocks:
            del blocks[ball_xy]

            if abs(self.vx) > abs(self.vy):
                self.vx = -self.vx
            else:
                self.vy = -self.vy

    def draw(self, display):
        display.set_pixel(int(self.x), int(self.y), self.color)

class Block:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        r, g, b = hsv_to_rgb(random.random(), 1, 1)1
        #self.color = (int(r*VALUE), int(g*VALUE), int(b*VALUE))
        self.color = (20, 20, 0)

    def draw(self, display):
        display.set_pixel(int(self.x), int(self.y), self.color)

blocks = {}
ball = Ball(8*9-1, 4, 0.7, 0.2, 0.5)

for y in range(8):
    for x in range(0, 10):
        block = Block(x, y)
        blocks[(x, y)] = block

while True:
    display.strip.fill((0, 0, 0))
    ball.update(blocks)
    ball.draw(display)
    for block in blocks.values():
        block.draw(display)

    display.write()
