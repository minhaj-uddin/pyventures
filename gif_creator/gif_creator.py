import imageio.v3 as iio
from PIL import Image
import numpy as np

files = ["mage-1.jpg", "mage-2.jpg", "mage-3.jpg"]

first_img = Image.open(files[0])
target_size = first_img.size

images = []

for file in files:
    img = Image.open(file).resize(target_size)
    images.append(np.array(img))

iio.imwrite('slideshow.gif', images, duration=1, loop=1)
