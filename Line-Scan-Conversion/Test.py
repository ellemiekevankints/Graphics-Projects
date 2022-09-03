from PIL import Image

img = Image.new('RGB', (960, 600)) # the window is 320 x 240
pixels = img.load()
pixels[0,0] = (255,0,0)
img.show()  