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
from .. import _settings


_SNAP_POINTS = {
    # x bound, y bound, uv coords, padding multiplier
    'LEFTTOP': ['min', 'max', Vector((0, 1)), Vector((1, -1))],
    'CENTERTOP': ['center', 'max', Vector((.5, 1)), Vector((0, -1))],
    'RIGHTTOP': ['max', 'max', Vector((1, 1)), Vector((-1, -1))],
    'LEFTCENTER': ['min', 'center', Vector((0, .5)), Vector((1, 0))],
    'CENTER': ['center', 'center', Vector((.5, .5)), Vector((0, 0))],
    'RIGHTCENTER': ['max', 'center', Vector((1, .5)), Vector((-1, 0))],
    'LEFTBOTTOM': ['min', 'min', Vector((0, 0)), Vector((1, 1))],
    'CENTERBOTTOM': ['center', 'min', Vector((.5, 0)), Vector((0, 1))],
    'RIGHTBOTTOM': ['max', 'min', Vector((1, 0)), Vector((-1, 1))]
}

# padding will either be -1, 0, 1

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
        # TODO add as a property
        deltaU = uv_transform.translate_u
        deltaV = uv_transform.translate_v

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        _uvs.translate_uvs(bm, uv_layer, uvs, deltaU, deltaV)
        bmesh.update_edit_mesh(me)

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
        # TODO add as prop
        scaleU = uv_transform.scale_u
        scaleV = uv_transform.scale_v

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        _uvs.scale_uvs(bm, uv_layer, uvs, scaleU, scaleV)
        bmesh.update_edit_mesh(me)

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
    bl_idname = "uv.be_rotate"
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

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        _uvs.rotate_uvs(bm, uv_layer, uvs, self.angle)
        bmesh.update_edit_mesh(me)

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

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        bounding_box = _uvs.get_selection_bounding_box()
        scaleU = 1.00 / bounding_box.get('width')
        scaleV = 1.00 / bounding_box.get('height')
        _uvs.scale_uvs(bm, uv_layer, uvs, scaleU, scaleV)

        bounding_box = _uvs.get_selection_bounding_box()
        deltaU = -bounding_box.get('min').x
        deltaV = -bounding_box.get('min').y
        _uvs.translate_uvs(bm, uv_layer, uvs, deltaU, deltaV)
        
        bmesh.update_edit_mesh(me)
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

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        bounding_box = _uvs.get_selection_bounding_box()
        max_size = max(bounding_box.get("width"), bounding_box.get("height"))
        scalar = 1.00 / max_size
        _uvs.scale_uvs(bm, uv_layer, uvs, scalar, scalar)

        bounding_box = _uvs.get_selection_bounding_box()
        deltaU = -bounding_box.get('min').x
        deltaV = -bounding_box.get('min').y
        _uvs.translate_uvs(bm, uv_layer, uvs, deltaU, deltaV)
        bmesh.update_edit_mesh(me)
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

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        for island in islands:
            # get each selected uv on the island
            angle_sum = 0
            angle_count = 0
            edges = self.get_selected_island_edges(bm, island, uv_layer)

            for edge in edges:
                angle = math.degrees(_uvs.get_uv_edge_angle(edge[0].uv, edge[1].uv))
                angle_sum += angle
                angle_count += 1
            average_angle = angle_sum / angle_count
            _uvs.rotate_island(me, [island], uv_layer, average_angle)

        _uvs.restore_selection(bm, uv_layer)
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}

    def get_selected_island_edges(self, bm, island, uv_layer):
        faces = []
        for face in island:
            for loop in face.loops:
                if loop[uv_layer].select:
                    faces.append(face)
                    break

        uv_edges = []
        for face in faces:
            for loop in face.loops:
                uv_edge = []
                uv_edge.append(loop[uv_layer])
                uv_edge.append(loop.link_loop_next[uv_layer])
                uv_edges.append(uv_edge)
        
        selected_uv_edges = []
        for edge in uv_edges:
            if edge[0].select and not edge[0].pin_uv:
                if edge[1].select and not edge[1].pin_uv:
                    selected_uv_edges.append(edge)

        # TODO optimize
        return selected_uv_edges

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
        # center
        bounding_box = _uvs.get_selection_bounding_box()
        deltaX = .5 - bounding_box.get('center').x
        deltaY = .5 - bounding_box.get('center').y
        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        _uvs.translate_uvs(bm, uv_layer, uvs, deltaX, deltaY)
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
        settings = context.scene.betools_settings
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        bounds = _uvs.get_selection_bounding_box()
        x = _SNAP_POINTS.get(self.direction)[0]
        y = _SNAP_POINTS.get(self.direction)[1]
        target = _SNAP_POINTS.get(self.direction)[2]
        padding = _uvs.get_padding() / 4.0
        padding_x = _SNAP_POINTS.get(self.direction)[3].x * padding
        padding_y = _SNAP_POINTS.get(self.direction)[3].y * padding

        xDelta = target.x-bounds.get(x).x + padding_x
        yDelta = target.y-bounds.get(y).y + padding_y

        _uvs.translate_uvs(bm, uv_layer, uvs, xDelta, yDelta)

        bmesh.update_edit_mesh(me)
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

        padding = _uvs.get_padding() / 4.0
        translation = padding

        if self.axis == 'VERTICAL':
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
        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        scale = Vector(( -1.0, 1.0 )) if self.direction == "HORIZONTAL" else Vector(( 1.0, -1.0 ))
        _uvs.scale_uvs(bm, uv_layer, uvs, scale.x, scale.y)
        bmesh.update_edit_mesh(me)

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


class BETOOLS_OT_AddUVMap(bpy.types.Operator):
    bl_idname = "uv.be_add_uv_map"
    bl_label = "Add UV Map"
    bl_description = "Add another UV map/channel"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.uv_texture_add()
        maps = _settings.get_uv_maps(self, context)
        _settings.set_uv_map_dropdown(self, context, len(maps)-1)
        return({'FINISHED'})


class BETOOLS_OT_RemUVMap(bpy.types.Operator):
    bl_idname = "uv.be_remove_uv_map"
    bl_label = "Remove UV Map"
    bl_description = "Remove the current UV map/channel"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.mesh.uv_texture_remove()
        maps = _settings.get_uv_maps(self, context)
        _settings.set_uv_map_dropdown(self, context, len(maps)-1)
        return({'FINISHED'})


class BETOOLS_OT_ModifyUVChannel(bpy.types.Operator):
    bl_idname = "uv.be_modify_uv_channel"
    bl_label = "Edit Mode"
    bl_description = "Toggle to UV Map rename mode"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        _settings.uv_map_rename_mode = True
        return {'FINISHED'}


class BETOOLS_OT_RenameUVMap(bpy.types.Operator):
    bl_idname = "uv.be_uv_rename"
    bl_label = "Rename UV Map"
    bl_description = "Rename UV Map to rename property"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        for layer in bpy.context.object.data.uv_layers:
            if layer.name == context.scene.betools_settings.uv_map_new_name:
                self.report({'ERROR_INVALID_INPUT'}, "Name already exists!")
                return {'FINISHED'}

        index = int(context.scene.betools_settings.uv_maps)
        bpy.context.object.data.uv_layers[index].name = context.scene.betools_settings.uv_map_new_name
        context.scene.betools_settings.uv_map_new_name = "New UV Map"

        _settings.uv_map_rename_mode = False
        return {'FINISHED'}


class BETOOLS_OT_RandomizeUVs(bpy.types.Operator):
    bl_idname = "uv.be_uv_randomize"
    bl_label = "Rename UV Map"
    bl_description = "Slightly randomize the UV islands"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # TODO
        return {'FINISHED'}


bpy.utils.register_class(BETOOLS_OT_IslandSnap)
bpy.utils.register_class(BETOOLS_OT_UVCameraProject)
bpy.utils.register_class(BETOOLS_OT_UVTranslate)
bpy.utils.register_class(BETOOLS_OT_UVScale)
bpy.utils.register_class(BETOOLS_OT_UVRotate)
bpy.utils.register_class(BETOOLS_OT_Fill)
bpy.utils.register_class(BETOOLS_OT_Fit)
bpy.utils.register_class(BETOOLS_OT_OrientEdge)
bpy.utils.register_class(BETOOLS_OT_UVProject)
bpy.utils.register_class(BETOOLS_OT_IslandStack)
bpy.utils.register_class(BETOOLS_OT_IslandSort)
bpy.utils.register_class(BETOOLS_OT_FlipIsland)
bpy.utils.register_class(BETOOLS_OT_AddUVMap)
bpy.utils.register_class(BETOOLS_OT_RemUVMap)
bpy.utils.register_class(BETOOLS_OT_ModifyUVChannel)
bpy.utils.register_class(BETOOLS_OT_RenameUVMap)
bpy.utils.register_class(BETOOLS_OT_RandomizeUVs)
