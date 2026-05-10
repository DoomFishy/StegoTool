import os, sys
from PIL import Image, ImageFilter

img = Image.open('map.jpg')

print(img.format, img.size, img.mode)

box = (0,0,500,500)

# cut out a region in image
region = img.crop(box)

# Cut out a box im picture and rotate
rotate = region.transpose(Image.Transpose.ROTATE_180)
#img.paste(rotate, box)

# Change image RGB order
r, g, b = img.split()
rgb = Image.merge("RGB", (b,b,r))

# Resize
resize = img.resize((128,128))

# Convert to different Channels
convert = img.convert("L")

# Filter for image 
filter = img.filter(ImageFilter.GaussianBlur(radius=100))

