from unittest import TestCase
from imglyc import ImageL
import numpy as np


class TestImage(TestCase):
    def setUp(self):
        self.img = ImageL("1.jpg")
        self.img.img = np.array([[[1,1,1], [1,2,3]],
                                 [[2,2,2], [4,5,6]]])

    def test_grey_img(self):
        self.img.grey_img()
        b = True
        a = np.array([[[1, 1, 1], [2, 2, 2]],
                                 [[2, 2, 2], [5, 5, 5]]])
        if self.img.new_img.shape != a.shape:
            b = False
        for i in range(self.img.new_img.shape[0]):
            for j in range(self.img.new_img.shape[1]):
                for k in range(self.img.new_img.shape[2]):
                    if self.img.new_img[i,j,k] != a[i,j,k]:
                        b = False
        self.assertEqual(b, True)
