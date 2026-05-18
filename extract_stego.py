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

def findSize(cover, secret):
    # uses 4 bytes or 32 bits
    # uses R and G for now 
    cover_width, cover_height = cover.size

    random_width = random.randint(0, cover_width - 1)
    random_height = random.randint(0, cover_height - 1)
    
    current = 0

    rgb = cover.getpixel((random_width, random_height))

    r, g ,b = rgb

    bits = getBits(r, 1)

def extract_linear(cover, stego, bits):
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

stego_img = Image.open("stego_image.png")

extract_img = extract_prng(cover_img, stego_img, 1)
extract_img.save("secret_image.png")

