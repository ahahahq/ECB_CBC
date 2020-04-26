import numpy as np
import hashlib
import bitarray

class BlockEncryption:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def ecb_encryption(self, pixels, key, image_height, image_width):
        blocks = self.split_array_into_chunks(pixels, image_height, image_width)
        for i in range(len(blocks)):
            pixels = self.ecb_encrypt_block(pixels, blocks[i][0], blocks[i][1], blocks[i][2], blocks[i][3])
        return pixels

    def cbc_encryption(self, pixels, key, image_height, image_width):
        blocks = self.split_array_into_chunks(pixels, image_height, image_width)
        pixels = self.xor_block(pixels, blocks[0][0], blocks[0][1], blocks[0][2], blocks[0][3],
                                key)
        self.ecb_encrypt_block(pixels, blocks[0][0], blocks[0][1], blocks[0][2], blocks[0][3])
        for i in range(1, len(blocks)):
            prev_block_key = self.get_key_of_block(pixels, blocks[i - 1][0], blocks[i - 1][1], blocks[i - 1][2],
                                                   blocks[i - 1][3])
            pixels = self.xor_block(pixels, blocks[i][0], blocks[i][1], blocks[i][2], blocks[i][3],
                                            prev_block_key)
            pixels = self.ecb_encrypt_block(pixels, blocks[i][0], blocks[i][1], blocks[i][2], blocks[i][3])
        return pixels

    def ecb_encrypt_block(self, pixels, x1, y1, x2, y2):
        keyindex = 0
        block_key = self.get_key_of_block(pixels, x1, y1, x2, y2)
        h = hashlib.sha256()
        h.update(block_key)
        ba = bitarray.bitarray()

        ba.frombytes(h.hexdigest().encode('utf-8'))
        for i in range(x1, x2):
            for j in range(y1, y2):
                if ba[keyindex]:
                    pixels[i, j] = [0, 0, 0]
                else:
                    pixels[i, j] = [255, 255, 255]
                keyindex += 1
        return pixels

    def xor_block(self, pixels, x1, y1, x2, y2, key):
        keyindex = 0
        for i in range(x1, x2):
            for j in range(y1, y2):
                if key[keyindex]:
                    if pixels[i, j, 0] == 0 and pixels[i, j, 1] == 0 and pixels[i, j, 2] == 0:
                        pixels[i, j] = [255, 255, 255]
                    else:
                        pixels[i, j] = [0, 0, 0]
                else:
                    if pixels[i, j, 0] == 255 and pixels[i, j, 1] == 255 and pixels[i, j, 2] == 255:
                        pixels[i, j] = [255, 255, 255]
                    else:
                        pixels[i, j] = [0, 0, 0]
                keyindex += 1
        return pixels


    def get_key_of_block(self, pixels, x1, y1, x2, y2):
        block_key = np.zeros(self.width * self.height)
        keyindex = 0
        for i in range(x1, x2):
            for j in range(y1, y2):
                if pixels[i, j, 0] == 0 and pixels[i, j, 1] == 0 and pixels[i, j, 2] == 0:
                    block_key[keyindex] = 1
                else:
                    block_key[keyindex] = 0
                keyindex += 1
        return block_key

    def split_array_into_chunks(self, arr, arr_height, arr_width):
        result = []
        for i in range(0, arr_height, self.height):
            for j in range(0, arr_width, self.width):
                x1 = i
                y1 = j
                if j + self.width > arr_width:
                    y2 = j + (self.width - ((j + self.width) - arr.size[1]))
                else:
                    y2 = j + self.width
                if i + self.height > arr_height:
                    x2 = i + (self.height - ((i + self.height) - arr.size[0]))
                else:
                    x2 = i + self.height
                result.append([x1, y1, x2, y2])
        return result
