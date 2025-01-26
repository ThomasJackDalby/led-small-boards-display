import random
import time
from led_display import LedDisplay

display = LedDisplay(machine.Pin.board.GP28, boards=9)

while True:
    c = tuple(random.randint(0, 255) for _ in range(3))
    display.strip.fill(c)
    display.write()
    display.strip.fill((0, 0, 0))
    display.write()
    time.sleep(0.1)