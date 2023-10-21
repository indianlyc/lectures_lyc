import pytesseract
import pyautogui
import numpy as np
import serial

port = '/dev/pts/1'
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract'

old_msg = 0
msg = 0
with serial.Serial(port, 9600, timeout=5) as ser:
    for i in range(1000):
        pil_img = pyautogui.screenshot(region=(1315, 1005, 75, 25))#.save('filename.png')
        #exit()
        open_cv_image = np.array(pil_img)
        open_cv_image = open_cv_image[:, :, ::-1].copy() # Convert RGB to BGR
        img = open_cv_image
        text = pytesseract.image_to_string(img)
        try:
            msg = int(text.strip())
        except ValueError:
            pass
        msg = str(msg) + "\n"
        print(msg, end="")
        ser.write(msg.encode())


