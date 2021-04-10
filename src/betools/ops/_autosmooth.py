#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import math
from bpy.props import FloatProperty


class BETOOLS_OT_AutoSmooth(bpy.types.Operator):
    bl_label = "Automatically smooth hard edges"
    bl_description = "Smooth hard edges based on an angle value"
    bl_idname = "mesh.be_auto_smooth"
    bl_options = {'REGISTER', 'UNDO'}

    angle: FloatProperty(name="Angle", default=math.radians(45), min=math.radians(1), max=math.radians(180), subtype="ANGLE")

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.shade_smooth() 
        bpy.context.object.data.use_auto_smooth = True
        bpy.context.object.data.auto_smooth_angle = self.angle
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True


bpy.utils.register_class(BETOOLS_OT_AutoSmooth)
