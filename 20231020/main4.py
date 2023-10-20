import math
import bpy
import serial
import time
import cv2  # pip install opencv-python
import pytesseract
import pyautogui
import numpy as np

port = '/dev/ttyACM0'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

old_msg = 0
msg = 0
ard = serial.Serial(port, 9600, timeout=5)

for i in range(100):

    pil_img = pyautogui.screenshot()  # .save(r'filename.png')

    # img1 = cv2.imread("filename.png")
    open_cv_image = np.array(pil_img)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    img = open_cv_image[-75:-50, -605:-30, :]

    # cv2.imwrite("filename1.png", img)
    # print(img.shape)
    # exit()

    #    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    #    ret, thresh1 = cv2.threshold(gray, 0, 255, cv2.THRESH_OTSU | cv2.THRESH_BINARY_INV)
    #    rect_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (18, 18))
    #    dilation = cv2.dilate(thresh1, rect_kernel, iterations=1)
    #    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL,
    #                                           cv2.CHAIN_APPROX_NONE)

    #    im2 = img.copy()

    #    for cnt in contours:
    #        x, y, w, h = cv2.boundingRect(cnt)

    #        rect = cv2.rectangle(im2, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #        cropped = im2[y:y + h, x:x + w]
    text = pytesseract.image_to_string(img)

    try:
        msg = int(text.strip())
    except ValueError:
        pass
    # time.sleep(0.05)
    # msg = int(ard.readline().strip())

    ob = bpy.data.objects['Armature']
    ob.select_set(True)
    bpy.ops.object.mode_set(mode='POSE')
    pbone = ob.pose.bones["Bone.001"]
    pbone.bone.select = True
    pbone.rotation_mode = 'XYZ'
    axis = 'X'
    angle = msg - old_msg
    old_msg = msg
    pbone.rotation_euler.rotate_axis(axis, math.radians(angle))
    bpy.ops.object.mode_set(mode='OBJECT')
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=5)







