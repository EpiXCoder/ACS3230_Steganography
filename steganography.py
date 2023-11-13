"""
[Day 7] Assignment: Steganography
    - Turn in on Gradescope (https://make.sc/bew2.3-gradescope)
    - Lesson Plan: https://tech-at-du.github.io/ACS-3230-Web-Security/#/Lessons/Steganography

Deliverables:
    1. All TODOs in this file.
    2. Decoded sample image with secret text revealed
    3. Your own image encoded with hidden secret text!
"""
# TODO: Run `pip3 install Pillow` before running the code.
from PIL import Image, ImageDraw, ImageFont
import textwrap


def decode_image(path_to_png):

    # Open the image using PIL:
    encoded_image = Image.open(path_to_png)

    # Separate the red channel from the rest of the image:
    red_channel = encoded_image.split()[0]

    # Create a new PIL image with the same size as the encoded image:
    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()
    x_size, y_size = encoded_image.size

    # TODO: Using the variables declared above, replace `print(red_channel)` with a complete implementation:
    # print(red_channel)  # Start coding here!
    for x in range(x_size):
        for y in range(y_size):
            # Extract the least significant bit of the red value
            red_value = red_channel.getpixel((x, y))
            least_significant_bit = red_value & 1

            # Set the pixel value: all black or all white
            if least_significant_bit:
                pixels[x, y] = (255, 255, 255)
            else:
                pixels[x, y] = (0, 0, 0)


    # DO NOT MODIFY. Save the decoded image to disk:
    decoded_image.save("decoded_image.png")


def encode_image(path_to_png, text_to_hide):

    # Open the original image
    original_image = Image.open(path_to_png)
    encoded_image = original_image.copy()
    pixels = encoded_image.load()
    x_size, y_size = original_image.size

    # Create the text image
    text_image = write_text(text_to_hide, image_size=(x_size, y_size))
    text_pixels = text_image.load()

    # Encode the text image into the original image
    for x in range(x_size):
        for y in range(y_size):
            # Get the pixel from the text image
            text_pixel = text_pixels[x, y]

            # Get the current pixel's value from the original image
            original_pixel = list(pixels[x, y])

            # Modify the LSB of the red channel to match the text image's brightness
            lsb = 1 if text_pixel[0] > 128 else 0
            original_pixel[0] = (original_pixel[0] & ~1) | lsb

            # Update the pixel in the encoded image
            pixels[x, y] = tuple(original_pixel)

    # Save the encoded image
    encoded_image.save("encoded_image.png")


def write_text(text_to_write, image_size=(200, 100), font_size=40):

    # Create an image with a black background
    image = Image.new('RGB', image_size, 'black')
    draw = ImageDraw.Draw(image)

    # Load a font
    font_path = '/Library/Fonts/Arial.ttf'

    # Load a font with the specified size
    font = ImageFont.truetype(font_path, font_size)


    
    lines = textwrap.wrap(text_to_write, width=94) 

    # Draw each line of text
    y_text = 0
    for line in lines:
        line_width, line_height = draw.textsize(line, font=font)
        x_text = (image_size[0] - line_width) // 2
        draw.text((x_text, y_text), line, font=font, fill="white")
        y_text += line_height
    
    return image

decode_image("encoded_sample.png")

encode_image("goldendoodle.png", "Goldendoodle: a Mischievous Creature That Steals Your Bed, Heart, and Socks.")

# decode_image("encoded_image.png")