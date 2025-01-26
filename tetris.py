# tetris.py
# multiplayer tetris!

import math
import random
import time
from led_display import LedDisplay
from utils import hsv_to_rgb

display = LedDisplay(machine.Pin.board.GP28, boards=9)

COLORS = [tuple((int(i*255) for i in hsv_to_rgb(hue/10, 1, 0.25))) for hue in range(0, 10)]
BLACK = (0, 0, 0)

class BlockType:
    def __init__(self, data):
        self.data = []
        self.width = []
        self.height = []

        self.data.append(data)
        for i in range(1, 4):
            self.data.append([(dy, -dx) for dx, dy in self.data[i-1]])

        for i in range(0, 4):
            min_x = min(x for x, _ in self.data[i])
            min_y = min(y for _, y in self.data[i])
            max_x = max(x for x, _ in self.data[i])
            max_y = max(y for _, y in self.data[i])
            self.width.append(max_x - min_x)
            self.height.append(max_y - min_y)
            self.data[i] = set([(x - min_x, y - min_y) for x, y in self.data[i]])

SINGLE_BLOCK = BlockType([(0, 0)])

BLOCK_TYPES = [BlockType(data) for data in [
    [(0, 0), (1, 0), (0, 1), (1, 1)], # square
    [(0, 0), (0, 1), (0, 2), (1, 2)], # L
    [(0, 0), (0, 1), (0, 2), (-1, 2)], # L
    [(0, 0), (0, 1), (-1, 1), (-1, 2)], # squiggly
    [(0, 0), (0, 1), (1, 1), (1, 2)], # reverse squiggly
    [(0, 0), (0, 1), (0, 2), (0, 3)], # line
]]
class Block:
    def __init__(self, x, y, rotation, block_type, color):
        self.x = x
        self.y = y
        self.block_type = block_type
        self.rotation = rotation
        self.color = color
        self.solid = False

    @property
    def points(self):
        return self.block_type.data[self.rotation]

    @property
    def width(self):
        return self.block_type.width[self.rotation]
    
    @property
    def height(self):
        return self.block_type.height[self.rotation]
    
    def intersects(self, block) -> bool:
        """Checks whether this block intersects the other block"""
        if block == self: return False
        if not block.solid: return False
        if self.x + self.width < block.x or self.x > block.x + block.width: return False
        if self.y + self.height < block.y or self.y > block.y + block.height: return False
        for dx, dy in self.points:
            if (self.x - block.x + dx, self.y - block.y + dy) in block.points:
                return True
        return False

    def update(self, blocks, solid_cells):
        # update this function to just check if any of our points are in a solid cell 
        if self.solid: return False
        self.x += 1

        if self.x + self.width >= 8*9-1: # TODO: Update to display size
            self.solid = True
            return True

        for block in blocks:
            if self.intersects(block):
                self.x -= 1
                self.solid = True
                    
    def draw(self, display):
        for dx, dy in self.points:
            display.set_pixel(self.x + dx, self.y + dy, self.color)

blocks = [] # these are "active"/falling blocks
solid_cells = {} # these are static, or landed blocks

while True:
    if random.random() > 0.9:
        # randomly drop a new block
        block_type = random.choice(BLOCK_TYPES)
        rotation = random.randint(0, 3)
        y = random.randint(0, 8-block_type.height[rotation]-1)
        x = 0
        block = Block(x, y, rotation, block_type, random.choice(COLORS))
        blocks.append(block)

    display.strip.fill(BLACK)
    end = False
    for block in blocks:
        now_solid = block.update(blocks)
        block.draw(display)

        if now_solid:
            # add the cells to the solid
            for (dx, dy) in block.points:
                solid_cells[(block.x + dx, block.y + dy)] = block

            # check if a row
            for x in range(block.x, block.x+block.width+1):
                solid_row = True
                for y in range(0, 8):
                    if (x, y) not in solid_cells:
                        solid_row = False
                        break
                
                # TODO: Need to rewrite collision detection to just use solid_cells and colours
                # when a block touches a solid block, it just becomes a solid cell, and is removed from the "blocks" list.
                # solid cell just move down.
                if solid_row:
                    for y in range(0, 8):                  
                        test_block = solid_cells[(x, y)]         
                        for dx, dy in test_block.points:
                            tx = test_block.x + dx
                            ty = test_block.y + dy
                            if x == tx: # we're on the line that should vanish
                                del solid_cells[(x, test_block.y+dy)]
                            else: # turn the rest of the block into single bits
                                new_block = Block(test_block.x+dx, test_block.y+dy, 0, SINGLE_BLOCK, (255, 0, 0))
                                new_block.solid = True
                                solid_cells[(test_block.x+dx, test_block.y+dy)] = new_block
                                blocks.append(new_block)
                        if test_block in blocks: # TODO something  is up here..
                            blocks.remove(test_block)
                        display.set_pixel(x, y, (255, 255, 255))
            
            # check if its the end of the game
            for y in range(0, 8):
                pass

    # some end game code that needs rewriting
    # if end:
    #     for i in range(10):
    #         display.strip.fill((5, 5, 5))
    #         display.write()
    #         display.strip.fill((0, 0, 0))
    #         display.write()

    #     blocks = []
    # time.sleep(0.05)

    display.write()