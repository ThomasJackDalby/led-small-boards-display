# pip install Pillow
import os
from rich import print, traceback
traceback.install()
from PIL import Image, ImageFont, ImageDraw

# use a truetype font (.ttf)
# font file from fonts.google.com (https://fonts.google.com/specimen/Courier+Prime?query=courier)
# font_path = "fonts/Courier Prime/"
# font_name = "CourierPrime-Regular.ttf"
out_path = "images"

font_size = 12 # px
font_color = "#000000" # HEX Black

# Create Font using PIL
font = ImageFont.truetype("C:\\Users\\thoma\\AppData\\Local\\Microsoft\\Windows\Fonts\slkscr.ttf", font_size)

# Copy Desired Characters from Google Fonts Page and Paste into variable
desired_characters = "ABCČĆDĐEFGHIJKLMNOPQRSŠTUVWXYZŽabcčćdđefghijklmnopqrsštuvwxyzž1234567890‘?’“!”(%)[#]{@}/&\<-+÷×=>®©$€£¥¢:;,.*"

# Loop through the characters needed and save to desired location
for character in desired_characters:
    
    # Get text size of character
    left, top, right, bottom = font.getbbox(character)
    width = right - left
    height = bottom - top
    
    # Create PNG Image with that size #  (width, height),
    img = Image.new("RGB", (16, 16), color=(255, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Draw the character
    draw.text((-left, -top), str(character), font=font, fill=font_color)
    
    # Save the character as png
    file_name = str(ord(character)) + ".bmp"
    file_path = os.path.join(out_path, file_name)
    img.save(file_path, format="bmp")