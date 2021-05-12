#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class ExportSelection(bpy.types.Operator):
    bl_idname = "mesh.be_export_selected_fbx"
    bl_label = "Export Selected as FBX"
    bl_desctiprion = "Export selected meshes as an fbx"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.export_scene.fbx('INVOKE_DEFAULT', use_selection = True, object_types = {"MESH"})
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is not None and bpy.context.active_object.mode == "OBJECT":
            return True


class ExportScene(bpy.types.Operator):
    bl_idname = "mesh.be_export_scene_fbx"
    bl_label = "Export Scene as FBX"
    bl_desctiprion = "Export scene as an fbx"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.export_scene.fbx('INVOKE_DEFAULT')
        return {'FINISHED'}

# TODO Quick sculpt export
# TODO UE4 Export
# TODO Unity Export

bpy.utils.register_class(ExportSelection)
bpy.utils.register_class(ExportScene)
