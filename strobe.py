import math
import random
import time
from led_display import LedDisplay, load_font

font = load_font("font.json")
display = LedDisplay(machine.Pin.board.GP28, boards=9)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# t = 0
# while True:
#     x = int((display.total_columns-10) * (math.sin(0.1 * t) / 2.0 + 0.5)) + 4
#     display.strip.fill(BLACK)
#     for i in range(-5, 5):
#         display.set_column(x-i, WHITE)
#     display.set_text(10, 0, "SAUSAGES", font, BLACK)
#     display.write()
#     t += 1

# white = bytearray(64*3)
# black = bytearray(64*3)
# for i in range(len(white)): white[i] = 255

# while True:
#     for i in range(9):
#         color = white if random.random() > 0.5 else black
#         display.strip.buf[64*3*i:64*3*(i+1)] = color
#         display.write()

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

t = 0
hue = 0
while True:
    hue += 0.01
    if hue > 1: hue = 0
    value = (math.sin(0.5*t) + 1)/2

    r, g, b = hsv_to_rgb(hue, 1, value)
    display.strip.fill((int(r*255), int(g*255), int(b*255)))
    display.write()
    t += 1