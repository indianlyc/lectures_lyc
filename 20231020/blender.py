import math
import bpy
import serial
import time

old_msg = 0
msg = 0

# port = '/dev/ttyACM0'
port = "/dev/pts/3"
msg = 0
with serial.Serial(port, 9600, timeout=1) as ard:
    for i in range(1000):
        m = ard.readline().decode().strip()
        try:
            msg = int(m)
        except ValueError:
            pass
        # print(msg)

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
        # bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)