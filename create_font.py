# for a given font, want to create a compressed representation of it

import os
from rich import print, traceback
traceback.install()
from PIL import Image, ImageFont, ImageDraw

FONT_MODE = "1"
FONT_ANCHOR = "ls"
FONT_SIZE = 8
CHARACTERS = "abcdefghijklmnopqrstuvwxyz"

BITMAP_FOLDER_PATH = "images"

def extract_font_from_ttf(font_file_path):

    font_file_name = os.path.basename(font_file_path)
    font_name, font_ext = os.path.splitext(font_file_name)

    bitmap_folder_path = os.path.join(BITMAP_FOLDER_PATH, font_name)
    if not os.path.exists(bitmap_folder_path):
        os.mkdir(bitmap_folder_path)

    font = ImageFont.truetype(font_file_path, FONT_SIZE)
    
    for char in CHARACTERS:

        # width, height = font.getsize(char)
        # image = Image.new("RGBA", (width, height))
        # draw = ImageDraw.Draw(image)
        # draw.text((-2, 0), str(char), font=font, fill=(0, 0, 0))

        # text = 'test, test'
        bbox = font.getbbox(char, mode=FONT_MODE, anchor=FONT_ANCHOR)
        left, top, right, bottom = bbox
        width = right - left
        height = bottom - top
        print("-----")
        print(f"{char=}")
        print(f"{bbox=}")
        print(f"{width=} {height=}")

        image = Image.new('1', (width, height))
        mask = [x for x in font.getmask(char, mode=FONT_MODE, anchor=FONT_ANCHOR)]
        try:
            image.putdata(mask)
        except Exception as e:
            print(e)


        file_name = f"{ord(char)}.bmp"
        file_path = os.path.join(bitmap_folder_path, file_name)
        image.save(file_path, format="bmp")

if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser()

    args = parser.parse_args()

    main(args.font_name)
    