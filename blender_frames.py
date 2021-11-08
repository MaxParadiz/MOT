import bpy
import numpy as np
from pathlib import Path
import os

Nframes = int(os.sys.argv[4])


bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()   # Delete the object

scene = bpy.context.scene

scene.render.engine = "CYCLES" 
scene.render.resolution_percentage = 50

world = bpy.data.worlds['World']                                                                                                                                            
world.use_nodes = True                                                                                                                                                      
                                                                                                                                                                            
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value[:3] = (1, 1, 1)
bg.inputs[1].default_value = 1.0
#bpy.types.ColorManagedSequencerColorspaceSettings = 'sRGB'
#scene.render.film_transparent = True


camera_data = bpy.data.cameras.new(name='Camera')
camera_object = bpy.data.objects.new('Camera', camera_data)
#camera_object.data.type = 'ORTHO'
bpy.context.scene.collection.objects.link(camera_object)

scene.camera= camera_object
#scene.display_settings.display_device = 'sRGB'
scene.view_settings.view_transform = 'Raw'

#bpy.data.objects['Camera'].rotation_euler = [0,np.pi/2,np.pi/4]
#bpy.data.objects['Camera'].location = [10,10,0]
bpy.data.objects['Camera'].rotation_euler = [np.pi/2,np.pi/(2*6),0]
bpy.data.objects['Camera'].location = [0,-20,0]


mat = bpy.data.materials.new(name='Material')
mat.use_nodes=True
mat_nodes = mat.node_tree.nodes
mat_nodes['Principled BSDF'].inputs['Emission Strength'].default_value=1.0
mat_nodes['Principled BSDF'].inputs['Emission'].default_value=(1,0,0,1)
mat_nodes['Principled BSDF'].inputs['Base Color'].default_value=(1, 0, 0, 1.0)

for i in range(0,Nframes):
    bpy.ops.import_scene.obj(filepath=f"tmpOBJs/{i}.obj") # Import OBJ
    D = bpy.data
    WF = bpy.context.selected_objects[0].name
    o = D.objects[WF]
    o.material_slots[o.active_material_index].material = mat
    scene.render.filepath=f'tmpFrames/{i}.png'
    bpy.ops.render.render(write_still=1)
    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[WF].select_set(True)
    bpy.ops.object.delete()   # Delete the object
