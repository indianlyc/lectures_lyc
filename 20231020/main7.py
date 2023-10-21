import serial
import time

port = "/dev/pts/3"
msg = 0
with serial.Serial(port, 9600, timeout=1) as ard:
    for i in range(1000):
        m = ard.readline().decode().strip()
        try:
            msg = int(m)
        except ValueError:
            pass
        print(msg)
        time.sleep(0.01)