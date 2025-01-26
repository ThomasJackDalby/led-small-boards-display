import math
import random
import time
from led_display import LedDisplay

display = LedDisplay(machine.Pin.board.GP28, boards=9)

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
VALUE = 50
class Ball:
    def __init__(self, x, y, vx, vy, width, height, hue):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.height = height
        self.width = width
        
        r, g, b = hsv_to_rgb(hue, 1, 1)
        self.color = (int(r*VALUE), int(g*VALUE), int(b*VALUE))

    def update(self):
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

    def draw(self, display):
        for dx in range(self.width):
            for dy in range(self.height):
                display.set_pixel(int(self.x-self.width/2)+dx, int(self.y-self.height/2)+dy, self.color)

balls = []
for i in range(10):
    direction = random.random() * 2 * math.pi
    speed = 0.5 * (random.random() * 1 + 1)
    vx = speed*math.sin(direction)
    vy = speed*math.cos(direction)
    hue = random.random()
    width = random.randint(2, 4)
    height = random.randint(2, 4)
    ball = Ball(random.randint(0, 8*9), random.randint(0, 8*9), vx, vy, width, height, hue)
    balls.append(ball)

while True:
    # if random.random() > 0.9:
    #     display.strip.fill((255, 255, 255))
    # else:
    #     display.strip.fill((0, 0, 0))

    display.strip.fill((0, 0, 0))
    for ball in balls:
        ball.update()
        ball.draw(display)
    display.write()