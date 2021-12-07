#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

"""Helper functions"""

import bpy

def edit_mode(func):
    """Wrapper decorator for ensuring a function is run in edit mode
    """
    def wrapper(*args, **kwargs):
        previous_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='EDIT')
        result = func(*args, **kwargs)
        bpy.ops.object.mode_set(mode=previous_mode)
        return result
    return wrapper

def object_mode(func):
    """Wrapper decorator for ensuring a function is run in edit mode
    """
    def wrapper(*args, **kwargs):
        previous_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        result = func(*args, **kwargs)
        bpy.ops.object.mode_set(mode=previous_mode)
        return result
    return wrapper
