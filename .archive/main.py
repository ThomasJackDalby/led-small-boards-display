import time
from neopixel import Neopixel

NUMBER_OF_LEDS = 64

strip = Neopixel(NUMBER_OF_LEDS, 0, 28, "RGB")
strip.brightness(100)

while True:
    print("Update")
    strip.fill((255, 255, 255))
    time.sleep(0.5)
    strip.fill((0, 0, 0))
    time.sleep(0.5)