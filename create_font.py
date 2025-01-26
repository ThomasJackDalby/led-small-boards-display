# for a given font, want to create a compressed representation of it

import os
import json
from rich import print, traceback
traceback.install()
from PIL import Image, ImageFont, ImageDraw

FONT_MODE = "1"
FONT_ANCHOR = "ls"
FONT_SIZE = 8
CHARACTERS = "ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWXYZŽabcčćdđefghijklmnopqrsštuvwxyzž1234567890‘?’“!”(%)[#]{@}/&\<-+÷×=>®©$€£¥¢:;,.*"

BITMAP_FOLDER_PATH = "images"

def extract_font_from_ttf(font_file_path):

    font_file_name = os.path.basename(font_file_path)
    font_name, font_ext = os.path.splitext(font_file_name)
    if not font_ext == ".ttf":
        raise Exception()

    bitmap_folder_path = os.path.join(BITMAP_FOLDER_PATH, font_name)
    if not os.path.exists(bitmap_folder_path):
        os.mkdir(bitmap_folder_path)

    print(font_file_path)
    font = ImageFont.truetype(font_file_path, FONT_SIZE)
    
    font_json = {}
    for char in CHARACTERS:
        bbox = font.getbbox(char, mode=FONT_MODE, anchor=FONT_ANCHOR)
        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top

        # print("-----")
        # print(f"{char=}")
        # print(f"{bbox=}")
        # print(f"{width=} {height=}")

        # image = Image.new('1', (width, height))
        mask = [x for x in font.getmask(char, mode=FONT_MODE, anchor=FONT_ANCHOR)]

        font_json[str(ord(char))] = {
            "c": char,
            "b": ",".join(str(x) for x in bbox),
            "d": "".join('1' if x == 255 else '0' for x in mask)
        }

        # try:
        #     image.putdata(mask)
        # except Exception as e:
        #     print(e)

        # file_name = f"{ord(char)}.bmp"
        # file_path = os.path.join(bitmap_folder_path, file_name)
        # image.save(file_path, format="bmp")

    with open("comic-sans bold.json", "w") as file:
        json.dump(font_json, file, indent=4)

if __name__ == "__main__":
    extract_font_from_ttf("C:\\Users\\Tom\\Downloads\\Comic Sans MS Bold.ttf")
    # extract_font_from_ttf("fonts\\oldschool_pc_font_pack_v2.2_win\\ttf - Ac (aspect-corrected)\\AcPlus_IBM_BIOS.ttf")

    # import argparse
    # parser = argparse.ArgumentParser()

    # args = parser.parse_args()


    