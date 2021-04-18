#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
from bpy.props import EnumProperty, FloatVectorProperty
from mathutils import Vector
from ..utils import _uvs


_SNAP_POINTS = {
    'LEFTTOP': ['min', 'max', Vector((0, 1))],
    'CENTERTOP': ['center', 'max', Vector((.5, 1))],
    'RIGHTTOP': ['max', 'max', Vector((1, 1))],
    'LEFTCENTER': ['min', 'center', Vector((0, .5))],
    'CENTER': ['center', 'center', Vector((.5, .5))],
    'RIGHTCENTER': ['max', 'center', Vector((1, .5))],
    'LEFTBOTTOM': ['min', 'min', Vector((0, 0))],
    'CENTERBOTTOM': ['center', 'min', Vector((.5, 0))],
    'RIGHTBOTTOM': ['max', 'min', Vector((1, 0))]
}


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


# Transform

class BETOOLS_OT_UVTranslate(bpy.types.Operator):
    bl_idname = "uv.be_translate"
    bl_label = "Translate UVs"
    bl_description = "Translate UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        uv_transform = context.scene.uv_transform_properties
        deltaU = uv_transform.translate_u
        deltaV = uv_transform.translate_v

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        # may have to give the mesh too
        for island in islands:
            _uvs.translate_island(me, island, uv_layer, deltaU, deltaV)
        return {'FINISHED'}


class BETOOLS_OT_UVScale(bpy.types.Operator):
    bl_idname = "uv.be_scale"
    bl_label = "Scale UVs"
    bl_description = "Scale UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        uv_transform = context.scene.uv_transform_properties
        scaleU = uv_transform.scale_u
        scaleV = uv_transform.scale_v

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        for island in islands:
            _uvs.scale_island(me, island, uv_layer, scaleU, scaleV)
        return {'FINISHED'}


class BETOOLS_OT_UVRotate(bpy.types.Operator):
    bl_idname = "uv.be_rotate"
    bl_label = "Rotate UVs"
    bl_description = "Rotate UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        uv_transform = context.scene.uv_transform_properties
        angle = uv_transform.angle

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        for island in islands:
            _uvs.rotate_island(me, island, uv_layer, angle)

        return {'FINISHED'}


class BETOOLS_OT_Crop(bpy.types.Operator):
    pass


class BETOOLS_OT_Fill(bpy.types.Operator):
    pass


class BETOOLS_OT_Rect(bpy.types.Operator):
    pass


class BETOOLS_OT_IslandSnap(bpy.types.Operator):
    bl_idname = "uv.be_textools_snap_island"
    bl_label = "Snap Islands"
    bl_description = "Snap islands to different positions on the grid"
    bl_options = {'REGISTER', 'UNDO'}

    direction : bpy.props.StringProperty(
        name='Direction',
        default='TOPLEFT'
        )

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        #Only in Edit mode
        if bpy.context.active_object.mode != 'EDIT':
            return False
        #Requires UV map
        if not bpy.context.object.data.uv_layers:
            return False
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        return True

    def execute(self, context):

        island = _uvs.getSelectedIslands()
        if not island:
            return {'FINISHED'}
        bounds = _uvs.getIslandBoundingBox(island)

        x = _SNAP_POINTS.get(self.direction)[0]
        y = _SNAP_POINTS.get(self.direction)[1]
        target = _SNAP_POINTS.get(self.direction)[2]

        xDelta = target.x-bounds.get(x).x
        yDelta = target.y-bounds.get(y).y

        # _uvs.translateIsland(island, xDelta, yDelta)

        bpy.ops.transform.translate(
            value=(xDelta, yDelta, 0),
            orient_type='GLOBAL',
            orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)),
            orient_matrix_type='GLOBAL',
            mirror=True,
            use_proportional_edit=False,
            proportional_edit_falloff='SMOOTH',
            proportional_size=1,
            use_proportional_connected=False,
            use_proportional_projected=False,
            release_confirm=True
            )

        return {'FINISHED'}


bpy.utils.register_class(BETOOLS_OT_IslandSnap)
bpy.utils.register_class(BETOOLS_OT_UVCameraProject)
bpy.utils.register_class(BETOOLS_OT_UVTranslate)
bpy.utils.register_class(BETOOLS_OT_UVScale)
bpy.utils.register_class(BETOOLS_OT_UVRotate)
