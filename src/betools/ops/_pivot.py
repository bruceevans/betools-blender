#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class CenterPivot(bpy.types.Operator):
    bl_label = "Center Pivot"
    bl_description = "Move the pivot point to the center of the object."
    bl_idname = "mesh.be_center_pivot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True


class Pivot2Cursor(bpy.types.Operator):
    bl_label = "Pivot to 3D Cursor"
    bl_description = "Move the pivot point to the 3D cursor"
    bl_idname = "mesh.be_pivot2cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True

# TODO Edit pivot
