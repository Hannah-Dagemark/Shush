from PIL import Image

img = Image.open("Main/input/car.jpg").convert("RGBA")
print (f"{img.getpixel((10,10))}")
print (f"{img.getpixel((10,10))[1]}")
img.putpixel((10,10), (255, 255, 255, 200))
print (f"{img.getpixel((10,10))}")