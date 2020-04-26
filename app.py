from PIL import Image
import numpy as np
from BlockEncryption import BlockEncryption

width = 4
height = 4

block_encryption = BlockEncryption(width, height)


def generate_key(size):
    return np.random.randint(0, 2, size)


key_file = open('key.txt', 'w+')
key = generate_key(width * height)
key_file.write(str(key))

im = Image.open('plain.bmp')

image_height = im.size[0]
image_width = im.size[1]

ecb_pixels = np.array(im)
cbc_pixels = np.array(im)


ecb_pixels = block_encryption.ecb_encryption(ecb_pixels, key, image_height, image_width)
cbc_pixels = block_encryption.cbc_encryption(cbc_pixels, key, image_height, image_width)

gr_im1 = Image.fromarray(ecb_pixels).save('ecb_crypto.bmp')
gr_im2 = Image.fromarray(cbc_pixels).save('cbc_crypyo.bmp')

