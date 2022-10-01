from imglyc import ImageL

# imglyc.py

if __name__ == '__main__':
    img = ImageL("1.jpg")
    img.grey_img()
    img.save_img("1grey.jpg")
