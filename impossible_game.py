# impossible_game.py
# a poor implementation of the impossible game...!

import math
import random
import time
from led_display import LedDisplay

display = LedDisplay(machine.Pin.board.GP28, boards=9)

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
PLAYER = (50, 0, 0)
TERRAIN = (0, 50, 50)



class Block:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = TERRAIN

    def update(self):
        self.x -= 1

    def draw(self, display, undraw=False):
        color = BLACK if undraw else self.color
        for dx in range(self.width):
            for dy in range(self.height):
                display.set_pixel(self.x+dx, self.y+dy, color)

class Player:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.vx = 0
        self.vy = 0
        self.color = color
        self.invincible_color = WHITE
        self.invincible = 0

    def update(self, blocks):
        if self.y == 1 and len(blocks) > 0 and blocks[0].x <= self.x + 6 and random.random() > 0.75: 
            self.vy = 1

        self.y += self.vy
        if self.y > 1:
            self.vy -= 0.1
        else:
            self.vy = 0
            self.y = 1

        if self.invincible == 0:
            for block in blocks:
                if self.x >= block.x and self.x <= block.x + block.width:
                    if self.y >= block.y and self.y <= block.y + block.height:
                        self.x -= 1
                        self.invincible = 50
        else:
            self.invincible -= 1
    
    def draw(self, display, undraw=False):
        color = BLACK if undraw else (self.color if self.invincible == 0 else self.invincible_color)
        display.set_pixel(int(self.x), int(self.y), color)

players = [
    Player(14, 1, (0, 50, 0)),
    Player(13, 1, (50, 50, 0)),
    Player(12, 1, (0, 50, 50)),
    Player(11, 1, (50, 0, 50)),
    Player(10, 1, (50, 0, 0)),
]
blocks = []

display.set_row(0, TERRAIN)
display.write()
while True:
    for block in blocks: block.draw(display, True)
    for player in players: player.draw(display, True)

    if random.random() > 0.95:
        width = random.randint(1, 3)
        height = random.randint(1, 3)
        block = Block(8*9, 1, width, height)
        blocks.append(block)

    for block in blocks: block.update()
    for player in players: player.update(blocks)

    # remove blocks that are off the screen
    for i in range(len(blocks)-1, -1, -1):
        block = blocks[i]
        if block.x + block.width < 0:
            blocks = blocks[:i] + blocks[i+1:]
    
    # remove players that are off the screen
    for i in range(len(players)-1, -1, -1):
        player = players[i]
        if player.x < 0:
            players = players[:i] + players[i+1:]
            display.strip.fill(player.color)
            display.write()
            display.strip.fill(BLACK)
            display.set_row(0, TERRAIN)
            display.write()


    for block in blocks: block.draw(display)
    for player in players: player.draw(display)
    display.write()