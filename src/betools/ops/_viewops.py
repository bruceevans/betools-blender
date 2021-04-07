#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class ToggleWireFrame(bpy.types.Operator):
    bl_idname = "mesh.be_toggle_wireframe"
    bl_label = "Toggle Wireframe"
    bl_description = "Toggle wireframe mode on and off"
    bl_options = {'REGISTER', 'UNDO'}

    def toggle_wireframe(self, context):
        if context.space_data.overlay.show_wireframes:
            context.space_data.overlay.show_wireframes = False
        else:
            context.space_data.overlay.show_wireframes = True

    def execute(self, context):
        self.toggle_wireframe(context)
        return{'FINISHED'}


class ToggleFaceOrientation(bpy.types.Operator):
    bl_idname = "mesh.be_toggle_fo"
    bl_label = "Toggle Face Orientation"
    bl_description = "Toggle face orientation shading mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        if context.space_data.overlay.show_face_orientation:
            bpy.context.space_data.overlay.show_face_orientation = False
        else:
            bpy.context.space_data.overlay.show_face_orientation = True
        return {"FINISHED"}
