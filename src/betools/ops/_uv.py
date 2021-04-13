#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class BETOOLS_OT_UVCameraProject(bpy.types.Operator):
    bl_idname = "mesh.be_uv_camera_project"
    bl_label = "Project Camera"
    bl_description = "Project UVs from camera"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)
        return {'FINISHED'}


class BETOOLS_OT_UVXProject(bpy.types.Operator):
    pass


class BETOOLS_OT_UVYProject(bpy.types.Operator):
    pass

