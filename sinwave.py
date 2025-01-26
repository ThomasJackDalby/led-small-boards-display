import math
import random
import time
from led_display import LedDisplay

display = LedDisplay(machine.Pin.board.GP28, boards=9)
WHITE = (5, 5, 5)
t = 0
display.strip.fill((0, 0, 0))
display.write()

# while True:
#     display.strip.fill((0, 0, 0))
#     display.write()
#     time.sleep(0.1)
#     display.strip.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
#     display.write()

colours = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    # (255, 255, 0),
    # (0, 255, 255),
    # (255, 0, 255),
]

while True:

    display.strip.fill((0, 0, 0))
    for i, colour in enumerate(colours):

        for x in range(0, 8*9):
            y = int(3.5 * math.sin((x+t+2*i)/2) + 4)
            display.set_pixel(x, y, colour)
    display.write()
    t += 1