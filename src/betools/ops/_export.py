#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy

from .. import _settings
from .. utils import _engine


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
        if context.object is None:
            return False
        if bpy.context.active_object.mode != "OBJECT":
            return False
        if _settings.edit_pivot_mode:
            return False
        return True


class ExportScene(bpy.types.Operator):
    bl_idname = "mesh.be_export_scene_fbx"
    bl_label = "Export Scene as FBX"
    bl_desctiprion = "Export scene as an fbx"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.export_scene.fbx('INVOKE_DEFAULT')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if bpy.context.active_object.mode != "OBJECT":
            return False
        if _settings.edit_pivot_mode:
            return False
        return True


class BETOOLS_OT_ChooseExport(bpy.types.Operator):
    bl_idname = "mesh.be_choose_export_folder"
    bl_label = "Choose Quick Export Path"
    bl_desctiprion = "Open a file dialog and choose the quick OBJ export path."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # TODO
        return {'FINISHED'}


class BETOOLS_OT_QuickExport(bpy.types.Operator):
    bl_idname = "mesh.be_quick_export"
    bl_label = "Quick Export"
    bl_description = """Quickly export the scene to an OBJ. Set the path in the preferences.
        Meant to quickly get between other DCC packages. THIS WILL OVERWRITE THE EXISTING FILE AT THE PATH LOCATION.
        """
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        
        return {"FINISHED"}


class BETOOLS_OT_ExportGameMesh(bpy.types.Operator):
    bl_idname = "mesh.be_export_game_mesh"
    bl_label = "Export Selection for Game Engine"
    bl_desctiprion = "Export selection for your selected game engine (in prefs)"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.betools_settings
        engine = getattr(_engine, "{}".format(settings.game_engine))
        engine_mesh_export_args = engine.get('MESH_EXPORT')

        bpy.ops.export_scene.fbx('INVOKE_DEFAULT', **engine_mesh_export_args)
        return {'FINISHED'}


class BETOOLS_OT_ExportGameAnim(bpy.types.Operator):
    bl_idname = "mesh.be_export_game_anim"
    bl_label = "Export Animation"
    bl_desctiprion = "Export animation for the selected game engine. Selectable in Be Tools Addon prefs."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.betools_settings
        engine = getattr(_engine, "{}".format(settings.game_engine))
        engine_anim_export_args = engine.get('ANIM_EXPORT')

        bpy.ops.export_scene.fbx('INVOKE_DEFAULT', **engine_anim_export_args)
        return {'FINISHED'}


# TODO Quick sculpt export
# TODO UE4 Export
# TODO Unity Export


bpy.utils.register_class(ExportSelection)
bpy.utils.register_class(ExportScene)
bpy.utils.register_class(BETOOLS_OT_ChooseExport)
bpy.utils.register_class(BETOOLS_OT_QuickExport)
bpy.utils.register_class(BETOOLS_OT_ExportGameMesh)
bpy.utils.register_class(BETOOLS_OT_ExportGameAnim)
