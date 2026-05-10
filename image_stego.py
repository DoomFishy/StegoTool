import os, sys
from PIL import Image, ImageFilter

cover_img = Image.open("cover_map.jpg")
stego_img = Image.open("stego_map.jpg")

print(f"Cover Image: {cover_img.format}, {cover_img.size}, {cover_img.mode}")

rgb = cover_img.getpixel((0,0))

r, g, b = rgb

binary_r = format(r, "08b")
binary_g = format(g, "08b")
binary_b = format(b, "08b")

print(f"Binary: R:{binary_r}, G{binary_g}, B:{binary_b}")


# Assume Image is same size or smaller
def stego(cover, stego, bits):
    # Cartersian Plane (0,0) is top left
    cover_width, cover_height = cover.size
    stego_width, stego_height = stego.size

    # Printer style :)
    for i in range(cover_height):
        for j in range(cover_width):
            cover_pixel = cover.getpixel((i, j))
            
            cover_rgb = getBinaryRGB(cover_pixel)

            if i < stego_height and j < stego_width: # only modifying pixels that the stego image covers
                stego_pixel = stego.getpixel((i, j))
                stego_rgb = getBinaryRGB(stego_pixel)

                #need to get amount of LSB bits from stego to cover 

            return 0

def getBinaryRGB(pixel):
    r, g, b = rgb

    binary_r = format(r, "08b")
    binary_g = format(g, "08b")
    binary_b = format(b, "08b")

    return binary_r, binary_g, binary_b
    
stego(cover_img, stego_img, 1)


