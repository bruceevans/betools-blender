#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy

from .. import _settings


class BETOOLS_OT_ToggleWireFrame(bpy.types.Operator):
    bl_idname = "mesh.be_toggle_wireframe"
    bl_label = "Toggle Shaded Wireframe"
    bl_description = "Toggle shaded wireframe mode on and off"
    bl_options = {'REGISTER', 'UNDO'}

    def toggle_wireframe(self, context):
        if context.space_data.overlay.show_wireframes:
            context.space_data.overlay.show_wireframes = False
        else:
            context.space_data.overlay.show_wireframes = True

    def execute(self, context):
        self.toggle_wireframe(context)
        return{'FINISHED'}


class BETOOLS_OT_ToggleShaded(bpy.types.Operator):
    bl_idname = "mesh.be_toggle_shaded"
    bl_label = "Toggle Shaded"
    bl_description = "Toggle shaded mode on and off"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if bpy.context.space_data.shading.type == 'SOLID':
            bpy.context.space_data.shading.type = 'WIREFRAME'
        else:
            bpy.context.space_data.shading.type = 'SOLID'
        return {'FINISHED'}


class BETOOLS_OT_ToggleFaceOrientation(bpy.types.Operator):
    bl_idname = "mesh.be_toggle_fo"
    bl_label = "Toggle Face Orientation"
    bl_description = "Toggle face orientation shading mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.space_data.overlay.show_face_orientation:
            bpy.context.space_data.overlay.show_face_orientation = False
        else:
            bpy.context.space_data.overlay.show_face_orientation = True
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        return True


bpy.utils.register_class(BETOOLS_OT_ToggleWireFrame)
bpy.utils.register_class(BETOOLS_OT_ToggleShaded)
bpy.utils.register_class(BETOOLS_OT_ToggleFaceOrientation)
