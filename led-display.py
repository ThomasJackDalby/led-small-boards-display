import machine
from neopixel import NeoPixel

class LedFont:

    def __init__(self, data):
        self.data = data

    def get_mask(self, char):
        return self.data[char]["m"]

def load_font(file_path):
    pass
    # loads font from json

class LedDisplay:
    def __init__(self, pin, rows=8, columns=8, boards=1):
        self.rows_per_board = rows
        self.columns_per_board = columns
        self.number_of_boards = boards
        self.leds_per_board = self.rows_per_board * self.columns_per_board
        self.number_of_leds = self.leds_per_board * self.number_of_boards

        self.strip = NeoPixel(pin, self.number_of_leds)

    def get_index(self, x, y):
        return x * self.rows_per_board + y

    def set_pixel(self, x, y, color):
        index = self.get_index(x, y)
        self.strip[index] = color

    def set_column(self, x, color):
        index = x
        y = 0
        while y < self.columns_per_board:
            index += 1
            self.strip[index] = color
            y += 1

    def set_row(self, y, color):
        index = y
        x = 0
        while x < self.rows_per_board:
            index += self.rows_per_board
            self.strip[index] = color
            x += 1

    def draw_text(self, x, y, font, text, stroke):
        for char in text:
            char_data = font.get_char(char)
            left, top, right, bottom = char_data.get_bbox()
            # unfinished
            for value in char_data.mask:
                if value:
                    self.set_pixel(x, y, stroke)
                x += 1
                if x >= right: x = left


    
    


    

