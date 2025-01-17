import neopixel
import time

NUMBER_OF_LEDS = 64

# 32 LED strip connected to X8.
pin = machine.Pin.board.GP28
leds = neopixel.NeoPixel(pin, NUMBER_OF_LEDS)

# current_led = 0
# while True:
#     print(f"LED {current_led}")
#     leds[(current_led - 1) % NUMBER_OF_LEDS] = (0, 0, 0)
#     leds[current_led] = (255, 0, 0)
#     current_led = (current_led + 1) % NUMBER_OF_LEDS
#     leds.write()
#     time.sleep(0.1)

current_led = 0
while True:
    leds.fill((0, 0, 0))
    leds.write()
    time.sleep(1)

    leds.fill((0, 255, 255))
    leds.write()
    time.sleep(1)


# for i in range(NUMBER_OF_LEDS):
#     n[i] = (0, 0, 0, 50)

# # Update the strip.
# n.write()