# need a letter to pixels map
# always miss one row between characters
# characters always go to the edge of their map
# they don't have to be the same width

import os
import json
from bmp_reader import BMPReader

FONT = {}

with open("font/index.json", "r") as file:
    index = json.load(file)

    for char in index:
        file_path = index[char]
        FONT[char] = BMPReader(file_path)

for char in FONT:
    print(char)
