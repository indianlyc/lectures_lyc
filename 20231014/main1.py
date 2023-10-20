import bpy
import random
import math




bpy.context.scene.tool_settings.transform_pivot_point = 'BOUNDING_BOX_CENTER'
cubes = []
for i in range(5):
    bpy.ops.mesh.primitive_cube_add(enter_editmode=False, align='WORLD', 
                                    location=(0, 0, 0), 
                                    scale=(1, 1, 1))

    cubes.append(bpy.context.selected_objects[0])
    cubes[-1].location = (5, 5, i*5)
    cubes[-1].select_set(False)
    
    

for j in range(100):
    for i, e in enumerate([bpy.data.objects[el] for el in bpy.data.objects.keys() if el[:4] == "Cube"]):
        e.select_set(True)
        #bpy.context.view_layer.objects.active = e
        bpy.ops.object.origin_set(type="ORIGIN_CURSOR")
        bpy.ops.transform.rotate(value = 0.6 + i*0.2, orient_axis="Z", orient_type="CURSOR")
        e.select_set(False)

        
    bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=5)
    
    
