# code.py - test script to just turn an LED on/off

import digitalio
import time

led = digitalio.DigitalInOut(machine.Pin.board.LED)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)