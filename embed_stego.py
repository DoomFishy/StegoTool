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
from bitarray import bitarray

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
        bit_secret = (secret >> i) & 1 # get bit from position i

        if (bit_secret == 1):
            cover = cover | (1 << i) # change to 1
            #print("added 1 ", i)
        else:
            cover = cover & ~(1 << i) # change to 0
            #print("added 0 ", i)

    return cover

def swapBits(cover_rgb, secret_rgb, bits):
    secret_r, secret_g, secret_b = secret_rgb
    cover_r, cover_g, cover_b = cover_rgb

    r = setBits(cover_r, secret_r, 0, bits)
    g = setBits(cover_g, secret_g, 0, bits)
    b = setBits(cover_b, secret_b, 0, bits)

    new_rgb = r, g, b

    #print("----------------")
    return new_rgb

# build bits from back to front
# 
def hideSize(cover, secret):
    # uses 4 bytes or 32 bits
    # uses R and G for now 
    cover_width, cover_height = cover.size
    secret_width, secret_height = secret.size

    width_arr = bitarray(format(secret_width, "08b"))
    height_arr = bitarray(format(secret_height, "08b"))

    


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
                if i < secret_height: # only modifying pixels that the stego image covers
                    if j < secret_width:

                        width : int = random.randint(0, cover_width - 1)
                        height : int = random.randint(0, cover_height - 1)

                        secret_rgb = secret.getpixel((j, i))
                        cover_rgb = cover.getpixel((width, height))


                        new_rgb = swapBits(cover_rgb, secret_rgb, bits)

                        stego_img.putpixel((width, height), new_rgb)

                        progress.update(task, advance = 1)

                else:
                    return 0
            
hideSize(cover_img,secret_img)

stego_prng(cover_img, secret_img, 1)
stego_img.save("stego_image.png")

