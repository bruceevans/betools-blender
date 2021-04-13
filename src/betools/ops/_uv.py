#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from bpy.props import EnumProperty
from mathutils import Vector


class BETOOLS_OT_UVCameraProject(bpy.types.Operator):
    bl_idname = "mesh.be_uv_camera_project"
    bl_label = "Project Camera"
    bl_description = "Project UVs from camera position"
    bl_options = {'REGISTER', 'UNDO'}

    mode : EnumProperty(
        name="Mode",
        default='CAM',
        items=[
            ('CAM', 'CAM_PROJECT', 'Project from current camera position'),
            ('FRONT', 'FRONT_PROJECT', 'Project from the front ortho view'),
            ('TOP', 'TOP_PROJECT', 'Project from the top ortho view'),
            ('RIGHT', 'RIGHT_PROJECT', 'Project from the right ortho view')
        ]
    )

    def execute(self, context):
        if self.mode == 'CAM':
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=False)
            return {'FINISHED'}
        else:
            bpy.ops.view3d.view_axis(type=self.mode, align_active=False, relative=False)
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)

        return {'FINISHED'}


class BETOOLS_OT_Crop(bpy.types.Operator):
    pass


class BETOOLS_OT_Fill(bpy.types.Operator):
    pass


class BETOOLS_OT_Rect(bpy.types.Operator):
    pass


bpy.utils.register_class(BETOOLS_OT_UVCameraProject)
