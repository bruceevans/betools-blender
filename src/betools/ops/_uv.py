#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
import math
from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
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

# TODO export layout to image
# TODO show distortion
# TODO minimize stretch? Relax?
# TODO udim?
# TODO pin/unpin


class BETOOLS_OT_UVCameraProject(bpy.types.Operator):
    bl_idname = "mesh.be_uv_camera_project"
    bl_label = "Project Camera"
    bl_description = "Project UVs from camera position"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.uv.project_from_view(camera_bounds=False, correct_aspect=True, scale_to_bounds=False)
        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_UVTranslate(bpy.types.Operator):
    """ Uses menu properties
    """

    bl_idname = "uv.be_translate"
    bl_label = "Translate UVs"
    bl_description = "Translate UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        uv_transform = context.scene.betools_settings
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

        for island in islands:
            _uvs.translate_island(me, island, uv_layer, deltaU, deltaV)
        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_UVScale(bpy.types.Operator):
    bl_idname = "uv.be_scale"
    bl_label = "Scale UVs"
    bl_description = "Scale UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        uv_transform = context.scene.betools_settings
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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_UVRotate(bpy.types.Operator):
    """ Gets angle from UI prop
    """

    bl_idname = "uv.be_rotate"
    bl_label = "Rotate UVs"
    bl_description = "Rotate UVs in UV space"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        uv_transform = context.scene.betools_settings
        angle = uv_transform.angle

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        _uvs.rotate_island(me, islands, uv_layer, angle)

        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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

        _uvs.rotate_island(me, islands, uv_layer, self.angle)
        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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
        if not uv_edges:
            self.report({'INFO'}, 'Select a UV edge')
            return {'FINISHED'}

        for edge in uv_edges:
            angle = math.degrees(_uvs.get_uv_edge_angle(edge[0].uv, edge[1].uv))
            angle_sum += angle
            angle_count += 1
        average_angle = angle_sum / angle_count
        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        
        _uvs.rotate_island(me, islands, uv_layer, average_angle)
        _uvs.restore_selection(bm, uv_layer)
        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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
        if not bpy.context.active_object:
            return False
        #Only in Edit mode
        if bpy.context.active_object.mode != 'EDIT':
            return False
        #Requires UV map
        if not bpy.context.object.data.uv_layers:
            return False
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_IslandSnap(bpy.types.Operator):
    bl_idname = "uv.be_snap_island"
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
        # Selective sync off
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

        for island in islands:
            _uvs.translate_island(me, island, uv_layer, xDelta, yDelta)

        return {'FINISHED'}


class BETOOLS_OT_IslandStack(bpy.types.Operator):
    bl_idname = "uv.be_stack"
    bl_label = "Stacks Islands"
    bl_description = "Stack two islands on top of each other"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        islands = _uvs.get_selected_islands(bm, uv_layer)

        if len(islands) < 2:
            self.report({'INFO'}, 'Select 2 or more UV islands')
            return {'FINISHED'}

        # default to the first index
        targetCenter = _uvs.get_island_bounding_box(islands[0], uv_layer).get('center')

        for i in range(len(islands)-1):
            index = i + 1
            bbox = _uvs.get_island_bounding_box(islands[index], uv_layer)
            deltaX = bbox.get('center').x - targetCenter.x
            deltaY = bbox.get('center').y - targetCenter.y
            _uvs.translate_island(me, islands[index], uv_layer, -deltaX, -deltaY)

        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_IslandSort(bpy.types.Operator):
    bl_idname = "uv.be_island_sort"
    bl_label = "Sort Islands"
    bl_description = "Sort islands vertically or horizontally"
    bl_options = {'REGISTER', 'UNDO'}

    axis : EnumProperty(
        name="Sort Axis",
        default='VERTICAL',
        items=[
            ('VERTICAL', 'Vertical', 'Sort islands vertically'),
            ('HORIZONTAL', 'Horizontal', 'Sort islands horizontally')
        ]
    )

    def _getWidth(self, island, uv_layer):
        return _uvs.get_island_bounding_box(island, uv_layer).get('width')

    def _getHeight(self, island, uv_layer):
        return _uvs.get_island_bounding_box(island, uv_layer).get('height')

    def execute(self, context):

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        islands = _uvs.get_selected_islands(bm, uv_layer)
        if not islands:
            self.report({'INFO'}, 'Select UV islands')
            return {'FINISHED'}

        padding = context.scene.betools_settings.sort_padding
        translation = padding

        if self.axis == 'VERTICAL':

            """
            for island in islands:
                # doing vertical sort, we want longest axis to be the width
                # sort
                bbox = _uvs.get_island_bounding_box(island, uv_layer)
                # TODO check for rotate
                if bbox.get('height') > bbox.get('width'):
                    # rotate by 90
                    tempList = []
                    tempList.append(island)
                    _uvs.rotate_island(me, tempList, uv_layer, 90)
                    bbox = _uvs.get_island_bounding_box(island, uv_layer)
            """
            # sort by width
            sortedIslands = sorted(
                islands,
                key=lambda k: _uvs.get_island_bounding_box(k, uv_layer).get('width'))
            for island in reversed(sortedIslands):
                # move to corner
                bbox = _uvs.get_island_bounding_box(island, uv_layer)
                delta = Vector((padding, 1.0 - translation)) - Vector(( bbox.get('min').x, bbox.get('max').y))
                _uvs.translate_island(me, island, uv_layer, delta.x, delta.y)
                translation += bbox.get('height') + padding
        else:
            """
            for island in islands:
                bbox = _uvs.get_island_bounding_box(island, uv_layer)
                if bbox.get('width') > bbox.get('height'):
                    # rotate by 90
                    tempList = []
                    tempList.append(island)
                    _uvs.rotate_island(me, tempList, uv_layer, 90)
                    bbox = _uvs.get_island_bounding_box(island, uv_layer)
            """
            # sort by width
            sortedIslands = sorted(
                islands,
                key=lambda k: _uvs.get_island_bounding_box(k, uv_layer).get('height'))
            for island in reversed(sortedIslands):
                # move to corner
                bbox = _uvs.get_island_bounding_box(island, uv_layer)
                delta = Vector(( translation , 1.0 - padding )) - Vector((bbox.get('min').x, bbox.get('max').y)) 
                _uvs.translate_island(me, island, uv_layer, delta.x, delta.y)
                translation += bbox.get('width') + padding

        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


class BETOOLS_OT_FlipIsland(bpy.types.Operator):
    bl_idname = "uv.be_flip"
    bl_label = "Sort Islands"
    bl_description = "Sort islands vertically or horizontally"
    bl_options = {'REGISTER', 'UNDO'}

    direction : EnumProperty(
        name="Sort Axis",
        default='VERTICAL',
        items=[
            ('VERTICAL', 'Vertical', 'Flip vertically'),
            ('HORIZONTAL', 'Horizontal', 'Flip horizontally')
        ]
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

        scale = Vector(( -1.0, 1.0 )) if self.direction == "HORIZONTAL" else Vector(( 1.0, -1.0 ))
        for island in islands:
            bbox = _uvs.get_island_bounding_box(island, uv_layer)
            delta = Vector(( -bbox.get('center').x, -bbox.get('center').y ))
            _uvs.translate_island(me, island, uv_layer, delta.x, delta.y)
            _uvs.scale_island(me, island, uv_layer, scale.x, scale.y)
            _uvs.translate_island(me, island, uv_layer, -delta.x, -delta.y)

        return {'FINISHED'}

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
        # Selective sync off
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        #Only in UV editor mode
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False

        return True


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
bpy.utils.register_class(BETOOLS_OT_IslandStack)
bpy.utils.register_class(BETOOLS_OT_IslandSort)
bpy.utils.register_class(BETOOLS_OT_FlipIsland)
