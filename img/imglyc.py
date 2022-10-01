from PIL import Image
from copy import deepcopy
import numpy as np


class ImageL:
    def __init__(self, filepath):
        with Image.open(filepath) as img:
            img.load()
        self.img = np.asarray(img)
        self.new_img = deepcopy(self.img)

    def save_img(self, filename):
        new_img = Image.fromarray(self.new_img)
        new_img.save(filename)

    def grey_img(self):
        n_a = np.zeros(self.img.shape, dtype=np.uint8)
        for irow in range(self.img.shape[0]):
            for icol in range(self.img.shape[1]):
                r = np.mean(self.img[irow, icol])
                n_a[irow, icol] = (r, r, r)
        self.new_img = n_a

    def upside_down(self):
        pass

    def turn_right(self):
        pass