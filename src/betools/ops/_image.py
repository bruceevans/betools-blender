#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################


import bpy
import bmesh
import math
from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
from mathutils import Vector
from ..utils import _uvs


class BETOOLS_OT_GetTexel(bpy.types.Operator):
    bl_idname = "uv.be_get_texel"
    bl_label = "Get Texel Density"
    bl_description = "Get the texel density of the selected UV island"
    bl_options = {'REGISTER', 'UNDO'}

    # TODO poll for image

    def execute(self, context):
        current_texture = _uvs.get_current_image()
        resolution = current_texture.size
        print(resolution)
        # texel density math
        return {'FINISHED'}


class BETOOLS_OT_SetTexel(bpy.types.Operator):
    bl_idname = "uv.be_set_texel"
    bl_label = "Set Texel Density"
    bl_description = "Set the texel density of the selected UV island"
    bl_options = {'REGISTER', 'UNDO'}

    # TODO poll for image

    def execute(self, context):
        current_texture = _uvs.get_current_image()
        resolution = current_texture.size
        print(resolution)
        # texel density math
        return {'FINISHED'}


# Cube Helper - .5m 1m 2m options
# 6' mannequin helper


bpy.utils.register_class(BETOOLS_OT_GetTexel)