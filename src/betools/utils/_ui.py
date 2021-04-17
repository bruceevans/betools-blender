
import os
import bpy


def GetUVView():
    for window in bpy.context.window_manager.windows:
        screen = window.screen
        for area in screen.areas:
            if area.type == 'IMAGE_EDITOR': 
                for region in area.regions:
                    if region.type == 'WINDOW': 
                        override = {'window': window, 'screen': screen, 'area': area, 'region': region, 'scene': bpy.context.scene, 'edit_object': bpy.context.edit_object, 'active_object': bpy.context.active_object, 'selected_objects': bpy.context.selected_objects}   # Stuff the override context with very common requests by operators.  MORE COULD BE NEEDED!
                        return override
    return None