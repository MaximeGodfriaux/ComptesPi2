from PIL import Image
import numpy as np

padding = 100

img = Image.open('images/sweden.jpg')
img_np = np.array(img)

shape = img_np.shape
new_shape = (shape[0] - padding, shape[1], shape[2])

new_img = img_np[padding:, :, :]

first_line = img_np[:padding, :, :]
last_line = img_np[-padding:, :, :]

for i in range(padding):
    factor = i / (padding - 1)
    new_img[new_shape[0] - padding + i, :, :] = factor * first_line[i] + (1 - factor) * last_line[i]

img = Image.fromarray(new_img)
img.save('images/sweden_blur.png')