import json
import time
from neopixel import NeoPixel

class LedDisplay:
    def __init__(self, pin, rows=8, columns=8, boards=1):
        self.rows_per_board = rows
        self.columns_per_board = columns
        self.number_of_boards = boards
        self.leds_per_board = self.rows_per_board * self.columns_per_board
        self.number_of_leds = self.leds_per_board * self.number_of_boards

        self.total_columns = columns * self.number_of_boards
        self.total_rows = rows
        self.strip = NeoPixel(pin, self.number_of_leds)

    def get_index(self, x, y):
        return x * self.rows_per_board + y

    def set_pixel(self, x, y, color):
        if x < 0 or x >= self.total_columns: return
        if y < 0 or y >= self.total_rows: return
        index = self.get_index(x, y)
        self.strip[index] = color

    def set_column(self, x, color):
        index = self.get_index(x, 0)
        y = 0
        while y < self.rows_per_board:
            if index < len(self.strip):
                self.strip[index] = color
            index += 1
            y += 1

    def set_row(self, y, color):
        index = y
        x = 0
        while x < self.total_columns:
            if index < len(self.strip):
                self.strip[index] = color
            index += self.rows_per_board
            x += 1

    def set_text(self, x, y, text, font, color=(255, 255, 255)):
        for char in text:
            offset = 0
            if char == " ":
                offset = 4
            else:
                font_char = font[char]
                offset = font_char.right
                if x > -8 and x < 8 * 10:
                    cx = 0
                    cy = -font_char.top
                    for i, c in enumerate(font_char.mask):
                        if c:
                            self.set_pixel(x + cx, cy, color)
                        cx += 1
                        if cx >= font_char.right:
                            cx = 0
                            cy -= 1
            x += offset
    
    def pan_left(self, number_of_columns=1):
        temp = self.strip.buf[:8*3]
        self.strip.buf[:-8*3] = self.strip.buf[8*3:]
        self.strip.buf[-8*3:] = temp

    def pan_right(self, number_of_columns=1):
        temp = self.strip.buf[-number_of_columns*8*3:]
        self.strip.buf[8*3:] = self.strip.buf[:-8*3]
        self.strip.buf[:number_of_columns*8*3] = temp

    def scroll_text(self, text, font, color=(5, 5, 5)):
        for char in text:
            if char == " ":
                for _ in range(4):
                    self.strip.buf[:-8*3] = self.strip.buf[8*3:]
                    self.strip.buf[(64*9-8)*3:] = bytearray(8*3)
                    self.write()
            else:
                font_char = font[char]
                for x in range(0, font_char.width):
                    self.strip.buf[:-8*3] = self.strip.buf[8*3:]
                    self.strip.buf[(64*9-8)*3:] = bytearray(8*3)

                    # extract right strip
                    for y in range(0, font_char.height):
                        mask_index = font_char.get_mask_index(x, y)
                        if font_char.mask[mask_index]:
                            self.set_pixel(8*9-1, y, color)
                    self.write()
        for _ in range(len(text)*8):
            self.strip.buf[:-8*3] = self.strip.buf[8*3:]
            self.strip.buf[(64*9-8)*3:] = bytearray(8*3)
            self.write()
    
    def flash_text(self, text, font, color=(5, 5, 5)):
        for word in text.split(" "):
            self.strip.fill((0, 0, 0))
            word_len = sum(font[c].width for c in word)
            self.set_text(int(8*9/2-word_len/2), 0, word, font, color)
            self.write()
            time.sleep(0.1)   

    def write(self):
        self.strip.write()

class Font:
    def __init__(self, data):
        self.data = data

    def __getitem__(self, char):
        if char in self.data:
            return self.data[char]
        return self.data["?"]

class Char:
    def __init__(self, data):
        self.data = data
        left, top, right, bottom = [int(x) for x in data["b"].split(",")]
        self.left = left
        self.top = top
        self.right = right
        self.bottom = bottom

        self.width = abs(self.right - self.left)
        self.height = abs(self.top - self.bottom)

        self.char = data["c"]
        self.mask = [c == "1" for c in data["d"]]

    def get_mask_index(self, x, y):
        return (self.height - y - 1) * self.width + x
    
def load_font(file_path):
    with open(file_path, "r") as file:
        font_data = json.load(file)

    font = {}
    for key, char_data in font_data.items():
        font[chr(int(key))] = Char(char_data)
    
    return Font(font)