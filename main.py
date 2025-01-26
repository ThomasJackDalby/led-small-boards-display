import network
from time import sleep
import machine
import time
import json
import random
from micropyserver import MicroPyServer
import utils

from led_display import LedDisplay, load_font

print("Loading FONT")
font = load_font("font.json")
display = LedDisplay(machine.Pin.board.GP28, boards=9)

print("Connecting to Network")
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect("YURT", "yurtyurt")
while wlan.isconnected() == False:
    print('Waiting for connection...')
    sleep(1)
print(wlan.ifconfig())

''' there should be a wi-fi connection code here '''

def hello_world(request):
    ''' request handler '''
    server.send("HELLO WORLD!")

def display_message(request):
    try:
        params = utils.get_request_query_params(request)
        message = params["message"]
        message = message.replace("+", " ")
        server.send("HTTP/1.0 200\r\n")

        text = "MESSAGE"
        for i in range(10):
            text = "INCOMING" if text == "MESSAGE" else "MESSAGE"
            c = tuple(random.randint(0, 255) for _ in range(3))
            display.strip.fill(c)
            display.set_text(20, 0, text, font, (0, 0, 0))
            display.write()
            display.strip.fill((0, 0, 0))
            c = tuple(random.randint(0, 255) for _ in range(3))
            display.set_text(10, 0, text, font, c)
            display.write()
            time.sleep(0.1)

        print(message)
        display.strip.fill((0, 0, 0))
        display.write()
        display.set_text(0, 0, message, font, color=(5, 5, 5))
        display.write()

        # if random.random() > 0.5:
        #     display.scroll_text(message, font, color=(5, 5, 5))
        # else:
        #     display.flash_text(message, font, color=(5, 5, 5))

    except Exception as e:
        print(e)
        server.send("HTTP/1.0 418\r\n")

server = MicroPyServer()
server.add_route("/message", display_message)
server.start()