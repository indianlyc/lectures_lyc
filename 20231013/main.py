import math
import bpy
ob = bpy.data.objects['Armature']
ob.select_set(True)
bpy.ops.object.mode_set(mode='POSE')
pbone = ob.pose.bones["Bone.001"]
pbone.bone.select = True
pbone.rotation_mode = 'XYZ'
axis = 'X'
angle = 45
pbone.rotation_euler.rotate_axis(axis, math.radians(angle))
bpy.ops.object.mode_set(mode='OBJECT')
