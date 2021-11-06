import bpy
import numpy as np
from pathlib import Path
import os



bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()   # Delete the object

scene = bpy.context.scene

scene.render.engine = "CYCLES" 
scene.render.resolution_percentage = 50

world = bpy.data.worlds['World']                                                                                                                                            
world.use_nodes = True                                                                                                                                                      
                                                                                                                                                                            
bg = world.node_tree.nodes['Background']
bg.inputs[0].default_value[:3] = (0, 0, 0)
bg.inputs[1].default_value = 1.0


camera_data = bpy.data.cameras.new(name='Camera')
camera_object = bpy.data.objects.new('Camera', camera_data)
bpy.context.scene.collection.objects.link(camera_object)

scene.camera= camera_object
scene.view_settings.view_transform = 'Raw'

bpy.data.objects['Camera'].rotation_euler = [np.pi/2,0,0]
bpy.data.objects['Camera'].location = [0,-25,0]



bpy.ops.import_scene.obj(filepath="tmpOBJs/0.obj") # Import OBJ
D = bpy.data
WF = bpy.context.selected_objects[0].name
o = D.objects[WF]
edens = bpy.data.materials['ElectronDensity']
o.material_slots[o.active_material_index].material = edens

area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
area.spaces[0].region_3d.view_perspective = 'CAMERA'
area.spaces[0].shading.type = 'RENDERED'
