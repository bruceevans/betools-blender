#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class BETOOLS_OT_AutoSmooth(bpy.types.Operator):
    bl_label = "Automatically smooth hard edges"
    bl_description = "Smooth hard edges based on an angle value"
    bl_idname = "mesh.be_auto_smooth"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, angle):
        self.angle = angle

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


class BETOOLS_OT_AutoSmooth30(BETOOLS_OT_AutoSmooth):
    bl_idname = "mesh.be_auto_smooth_30"
    def __init__(self):
        BETOOLS_OT_AutoSmooth.__init__(self, 0.523599)


class BETOOLS_OT_AutoSmooth45(BETOOLS_OT_AutoSmooth):
    bl_idname = "mesh.be_auto_smooth_45"
    def __init__(self):
        BETOOLS_OT_AutoSmooth.__init__(self, 0.785398)


class BETOOLS_OT_AutoSmooth60(BETOOLS_OT_AutoSmooth):
    bl_idname = "mesh.be_auto_smooth_60"
    def __init__(self):
        BETOOLS_OT_AutoSmooth.__init__(self, 1.0472)


bpy.utils.register_class(BETOOLS_OT_AutoSmooth)
bpy.utils.register_class(BETOOLS_OT_AutoSmooth30)
bpy.utils.register_class(BETOOLS_OT_AutoSmooth45)
bpy.utils.register_class(BETOOLS_OT_AutoSmooth60)
