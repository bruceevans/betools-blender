#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
import math
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

_PROJECTION_SWIZZLE = {
    'X': 'yz',
    'Y': 'xz',
    'Z': 'xy'
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
            bpy.ops.view3d.view_axis(type=self.mode, align_active=False, relative=False) # TODO code this separately
            bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=True)

        return {'FINISHED'}


# Transform

class BETOOLS_OT_UVTranslate(bpy.types.Operator):
    """ Uses menu properties
    """

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
    """ Gets angle from UI prop
    """

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

        #for island in islands:
        _uvs.rotate_island(me, islands, uv_layer, angle)

        return {'FINISHED'}


class BETOOLS_OT_UVRotate2(bpy.types.Operator):
    bl_idname = "uv.be_rotate2"
    bl_label = "Rotate UVs"
    bl_description = "Rotate UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    angle : bpy.props.IntProperty(
        name='angle',
        default=90
    )

    def execute(self, context):
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        #for island in islands:
        _uvs.rotate_island(me, islands, uv_layer, self.angle)

        return {'FINISHED'}


class BETOOLS_OT_Fill(bpy.types.Operator):
    bl_idname = "uv.be_fill"
    bl_label = "UV Fill"
    bl_description = "Fill the selected island to the entire 0-1 UV space"
    bl_options = {"REGISTER", "UNDO"}

    def execute(self, context):

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        bounding_box = _uvs.get_selection_bounding_box()

        scaleU = 1.00 / bounding_box.get('width')
        scaleV = 1.00 / bounding_box.get('height')

        for island in islands:
            _uvs.scale_island(me, island, uv_layer, scaleU, scaleV)

        bounding_box = _uvs.get_selection_bounding_box()
        deltaU = bounding_box.get('min').x
        delatV = bounding_box.get('min').y

        for island in islands:
            _uvs.translate_island(me, island, uv_layer, -deltaU, -delatV)

        return {'FINISHED'}


class BETOOLS_OT_Fit(bpy.types.Operator):
    bl_idname = "uv.be_fit"
    bl_label = "UV Fit"
    bl_description = "Uniformly scale the island to fit in the 0-1 UV space, no stretching."
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        bounding_box = _uvs.get_selection_bounding_box()

        max_size = max(bounding_box.get("width"), bounding_box.get("height"))
        scalar = 1.00 / max_size

        for island in islands:
            _uvs.scale_island(me, island, uv_layer, scalar, scalar)

        bounding_box = _uvs.get_selection_bounding_box()
        deltaU = bounding_box.get('min').x
        delatV = bounding_box.get('min').y

        for island in islands:
            _uvs.translate_island(me, island, uv_layer, -deltaU, -delatV)

        return {'FINISHED'}


class BETOOLS_OT_OrientEdge(bpy.types.Operator):
    bl_idname = "uv.be_orient_edge"
    bl_label = "Orient to Edge"
    bl_description = "Orient UV Island to selected edges"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        
        angle_sum = 0
        angle_count = 0

        uv_edges = _uvs.get_selected_uv_edges(bm, uv_layer)
        for edge in uv_edges:
            angle = math.degrees(_uvs.get_uv_edge_angle(edge[0].uv, edge[1].uv))
            angle_sum += angle
            angle_count += 1
        # TODO precheck the angle
        average_angle = angle_sum / angle_count
        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.rotate_island(me, islands, uv_layer, average_angle)
        _uvs.restore_selection(bm, uv_layer)
        return {'FINISHED'}


# Super gross but the op wouldn't auto run when fed the attribute
class BETOOLS_OT_UVProject(bpy.types.Operator):
    bl_idname = "uv.be_axis_project"
    bl_label = "UV Project"
    bl_description = "Project UVs from a given axis"
    bl_options = {'REGISTER', 'UNDO'}

    axis : EnumProperty(
        name="Axis",
        default='Y',
        items=[
            ('X', 'X', 'Project from the X ortho'),
            ('Y', 'Y', 'Project from the Y ortho'),
            ('Z', 'Z', 'Project from the Z ortho')
        ]
    )

    def execute(self, context):
        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        for face in bm.faces:
            if face.select:
                for loop in face.loops:
                    loop_uv = loop[uv_layer]
                    loop_uv.select = True
                    loop_uv.uv = getattr(loop.vert.co, _PROJECTION_SWIZZLE.get(self.axis))
        
        bmesh.update_edit_mesh(me)
        bpy.ops.uv.be_fit()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if not bpy.context.object.mode == 'EDIT':
            return False
        return True


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
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        islands = _uvs.get_selected_islands(bm, uv_layer)
        if not islands:
            return {'FINISHED'}
        # bounds = _uvs.getIslandBoundingBox(islands)
        bounds = _uvs.get_selection_bounding_box()

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
bpy.utils.register_class(BETOOLS_OT_UVRotate2)
bpy.utils.register_class(BETOOLS_OT_Fill)
bpy.utils.register_class(BETOOLS_OT_Fit)
bpy.utils.register_class(BETOOLS_OT_OrientEdge)
bpy.utils.register_class(BETOOLS_OT_UVProject)
