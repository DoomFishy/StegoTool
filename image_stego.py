# TO DO
# - Check for RGB or RGBA
# - Optimize it
# - MAYBE TERMINAL STUFF
# - Do error checking (too big secret image, etc)
# - spread bits hidden

#change = (a >> 2) | (b << 2)
#getPosition = (b >> 4) & 1
#setBit1 = b | (1 << 4)
#setBit0 = b & ~(1 << 4)
#print(f"{setBit0:08b}")

import os, sys, time, random

from PIL import Image, ImageFilter
from rich.progress import Progress, track

cover_img = Image.open(sys.argv[1])
secret_img = Image.open(sys.argv[2])    

stego_img = cover_img.copy()

print(f"Cover Image: {cover_img.format}, {cover_img.size}, {cover_img.mode}")
print(f"Secret Image: {secret_img.format}, {secret_img.size}, {secret_img.mode}")

cover_img = cover_img.convert("RGB")
secret_img = secret_img.convert("RGB")

password = None


# create random spacing on random.randint(a,b)
# create random bit weight on RGB instead of even weighted

if len(sys.argv) > 3:
    password = sys.argv[3]
    random.seed(password)


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
        bit_secret = (secret >> i) & 1

        if (bit_secret == 1):
            cover = cover | (1 << i) # change to 1
        else:
            cover = cover & ~(1 << i) # change to 0

    return cover

def swapBits(cover_rgb, secret_rgb, bits):
    secret_r, secret_g, secret_b = secret_rgb
    cover_r, cover_g, cover_b = cover_rgb

    cover_r = setBits(cover_r, secret_r, 0, bits)
    cover_g = setBits(cover_g, secret_g, 0, bits)
    cover_b = setBits(cover_b, secret_b, 0, bits)

    new_rgb = cover_r, cover_g, cover_b

    return new_rgb

# Assume Image is same size or smaller
def stego_linear(cover, secret, bits):
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

                        new_rgb = swapBits(cover_rgb, secret_rgb, bits)

                        stego_img.putpixel((j,i), new_rgb)

                        progress.update(task, advance = 1)

                else:
                    return 0

def stego_prng_gap(cover, secret, bits):
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

                        new_rgb = swapBits(cover_rgb, secret_rgb, bits)

                        gap_width : int = random.randint(0, cover_width - 1)

                        width = j + gap_width
                        height = i

                        try:
                            if width >= cover_width:
                                if height + 1 < cover_height:
                                    height = i + 1
                                else:
                                    height = 0
                                
                                width = gap_width
                            stego_img.putpixel((width, height), new_rgb)

                        except:
                            print("width: " + str(width) + " | " + "height: " + str(height))


                        progress.update(task, advance = 1)

                else:
                    return 0
            
def stego_prng(cover, secret, bits):
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

                        new_rgb = swapBits(cover_rgb, secret_rgb, bits)

                        gap_width : int = random.randint(0, cover_width - 1)
                        gap_height : int = random.randint(0, cover_height - 1)

                        stego_img.putpixel((gap_width, gap_height), new_rgb)


                        progress.update(task, advance = 1)

                else:
                    return 0
            
def getBits(pixel, end):
    mask = (1 << end) - 1

    return (pixel & mask)

def extractBits(pixel, bits):
    r, g, b = pixel

    stego_r = getBits(r, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255
    stego_g = getBits(g, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255
    stego_b = getBits(b, bits) * int(255 / (pow(2, bits) - 1)) # multiply to scale to 255


    rgb = stego_r, stego_g, stego_b
    return rgb

def extract_linear(stego, bits):
    stego_width, stego_height = secret_img.size
    extract_img = Image.new("RGB", (stego_width, stego_height), 0)

    with Progress() as progress:
        task = progress.add_task("Extracting Image...", total = (stego_height * stego_width))
        
        for i in range(stego_height):
            for j in range(stego_width):
                pixel = stego.getpixel((j,i))

                rgb = extractBits(pixel, bits)

                extract_img.putpixel((j,i), rgb)

                progress.update(task, advance = 1)


    return extract_img

def extract_prng_gap(cover, stego, bits):
    cover_width, cover_height = cover.size
    stego_width, stego_height = secret_img.size

    extract_img = Image.new("RGB", (stego_width, stego_height), 0)

    with Progress() as progress:
        task = progress.add_task("Extracting Image...", total = (stego_height * stego_width))
        
        for i in range(stego_height):
            for j in range(stego_width):
                gap_width : int = random.randint(0, cover_width - 1)
                gap_height: int = random.randint(0, cover_height - 1)

                width = j + gap_width
                height = i
                pixel = None

                if width >= cover_width:
                    if height + 1 < cover_height:
                        height = i + 1
                    else:
                        height = 0
                                
                    width = gap_width
                pixel = stego.getpixel((width, height))


                rgb = extractBits(pixel, bits)

                extract_img.putpixel((j, i), rgb)

                progress.update(task, advance = 1)


    return extract_img

def extract_prng(cover, stego, bits):
    cover_width, cover_height = cover.size
    stego_width, stego_height = secret_img.size

    extract_img = Image.new("RGB", (stego_width, stego_height), 0)

    with Progress() as progress:
        task = progress.add_task("Extracting Image...", total = (stego_height * stego_width))
        
        for i in range(stego_height):
            for j in range(stego_width):
                width : int = random.randint(0, cover_width - 1)
                height: int = random.randint(0, cover_height - 1)

                pixel = stego.getpixel((width, height))

                rgb = extractBits(pixel, bits)
                
                extract_img.putpixel((j, i), rgb)

                progress.update(task, advance = 1)


    return extract_img

stego_prng_gap(cover_img, secret_img, 1)
stego_img.save("stego_image.png")

"""

stego_img = Image.open("stego_image.png")

extract_img = extract_prng(cover_img, stego_img, 1)
extract_img.save("secret_image.png")

"""


#print(f"setting: {b:08b} to {a:08b}")
#test = setBits(a, b, 0, 1)
#print(f"{test:08b}")