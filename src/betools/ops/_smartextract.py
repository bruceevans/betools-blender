#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from .. import _settings


class BETOOLS_OT_SmartExtract(bpy.types.Operator):
    """ An operation to extract the selected faces from a mesh
        and create a new mesh from that selection
    """

    bl_idname = "mesh.smart_extract"
    bl_label = "Smart Extract"
    bl_description = "Extract selected faces into a new mesh.  Must be in face mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.duplicate()
        bpy.ops.object.mode_set(mode = 'EDIT')
        obj = bpy.context.selected_objects[0]
        bpy.ops.mesh.select_all(action ='INVERT')
        bpy.ops.mesh.delete(type='FACE')
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.mesh.be_center_pivot()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        sm = tuple(bpy.context.tool_settings.mesh_select_mode)
        if context.object is None:
            return False
        if not sm[2]:
            return False
        if _settings.edit_pivot_mode:
            return False
        if context.object.type != 'MESH':
            return False
        return True

bpy.utils.register_class(BETOOLS_OT_SmartExtract)
