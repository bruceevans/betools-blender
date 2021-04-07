#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy

from ..utils import _constants

class SmartMirror(bpy.types.Operator):
    bl_label = ""
    bl_description = ""
    bl_idname = "mesh.smart_mirror"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, direction, name):
        bl_label = str(name)
        bl_description = "Global mirror operation in the chosen axis"
        self.label = bl_label
        self.mirror_direction = direction

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.duplicate()
        bpy.ops.transform.mirror(
            orient_type='GLOBAL',
            constraint_axis=(self.mirror_direction),
            use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH',
            proportional_size=1,
            use_proportional_connected=False,
            use_proportional_projected=False
            )
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is not None:
            return


class SmartMirrorX(SmartMirror):
    bl_idname = "mesh.smart_mirror_x"
    def __init__(self):
        SmartMirror.__init__(self, _constants.MIRROR_MODES["X"], "Smart Mirror X")


class SmartMirrorY(SmartMirror):
    bl_idname = "mesh.smart_mirror_y"
    def __init__(self):
        SmartMirror.__init__(self, _constants.MIRROR_MODES["Y"], "Smart Mirror Y")


class SmartMirrorZ(SmartMirror):
    bl_idname = "mesh.smart_mirror_z"
    def __init__(self):
        SmartMirror.__init__(self, _constants.MIRROR_MODES["Z"], "Smart Mirror Z")