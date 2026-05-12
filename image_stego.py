import os, sys
import time

from PIL import Image, ImageFilter
from rich.progress import Progress, track

cover_img = Image.open("Images/cover_map.png")
secret_img = Image.open("Images/BNW.png")
stego_img = cover_img.copy()

print(f"Cover Image: {cover_img.format}, {cover_img.size}, {cover_img.mode}")
print(f"Secret Image: {secret_img.format}, {secret_img.size}, {secret_img.mode}")

cover_img = cover_img.convert("RGB")
secret_img = secret_img.convert("RGB")



# TO DO
# - Check for RGB or RGBA
# - Optimize it
# - MAYBE TERMINAL STUFF
# - Do error checking (too big secret image, etc)
# - Do the app stuff later

#change = (a >> 2) | (b << 2)
#getPosition = (b >> 4) & 1
#setBit1 = b | (1 << 4)
#setBit0 = b & ~(1 << 4)
#print(f"{setBit0:08b}")


def getBinaryRGB(pixel):
    r, g, b = pixel

    binary_r = format(r, "08b")
    binary_g = format(g, "08b")
    binary_b = format(b, "08b")

    return binary_r, binary_g, binary_b

# 0 is far right and end is far left
# Read right to left
def setBits(cover, secret, start : int, end : int):
    for i in range(start, end):
        bit_cover = (cover >> i) & 1
        bit_secret = (secret >> i) & 1

        if (bit_secret == 1):
            cover = cover | (1 << i) # change to 1
        else:
            cover = cover & ~(1 << i) # change to 0

    return cover

# Assume Image is same size or smaller
def stego(cover, secret, bits):
    # Cartersian Plane (0,0) is top left
    cover_width, cover_height = cover.size
    secret_width, secret_height = secret.size

    # Printer style :)
    with Progress() as progress:
        task = progress.add_task("Embedding Image...", total = (secret_height * secret_width))

        for i in range(cover_height):
            for j in range(cover_width):
                cover_rgb = cover.getpixel((j, i))
                
                if i < secret_height: # only modifying pixels that the stego image covers
                    if j < secret_width:
                        secret_rgb = secret.getpixel((j, i))

                        #need to get amount of LSB bits from stego to cover
                        secret_r, secret_g, secret_b = secret_rgb
                        cover_r, cover_g, cover_b = cover_rgb


                        cover_r = setBits(cover_r, secret_r, 0, bits)
                        cover_g = setBits(cover_g, secret_g, 0, bits)
                        cover_b = setBits(cover_b, secret_b, 0, bits)

                        new_rgb = cover_r, cover_g, cover_b

                        stego_img.putpixel((j,i), new_rgb)

                        progress.update(task, advance = 1)

                else:
                    return 0
            
def getBits(pixel, start, end):
    mask = (1 << end) - 1

    return (pixel & mask)

def extract(stego, bits):
    stego_width, stego_height = secret_img.size
    extract_img = Image.new("RGB", (stego_width, stego_height), 0)

    with Progress() as progress:
        task = progress.add_task("Extracting Image...", total = (stego_height * stego_width))
        
        for i in range(stego_height):
            for j in range(stego_width):
                pixel = stego.getpixel((j,i))

                r, g, b = pixel

                stego_r = getBits(r, 0, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255
                stego_g = getBits(g, 0, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255
                stego_b = getBits(b, 0, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255


                rgb = stego_r, stego_g, stego_b
                
                extract_img.putpixel((j,i), rgb)

                progress.update(task, advance = 1)


    return extract_img

stego(cover_img, secret_img, 1)
stego_img.save("stego_image.png")

stego_img = Image.open("stego_image.png")

extract_img = extract(stego_img, 1)
extract_img.save("secret_image.png")

#print(f"setting: {b:08b} to {a:08b}")
#test = setBits(a, b, 0, 1)
#print(f"{test:08b}")