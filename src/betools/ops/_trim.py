#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
from mathutils import Vector
from bpy.props import EnumProperty
from pprint import pprint
from ..utils import _uvs
from ..utils import _core
from .. import _settings


_DEPTH_THRESHOLD = 0.0001


class BETOOLS_OT_AssignTrimTemplate(bpy.types.Operator):
    """Set a template mesh for trim snapping"""

    bl_idname = "uv.be_trim_template"
    bl_label = "Create Trim Template"
    bl_description = "Select a template mesh for UV Trim snapping"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        if not bpy.context.active_object:
            return False
        if context.object.type != 'MESH':
            return False
        if not bpy.context.object.data.uv_layers:
            return False
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        if len(bpy.context.selected_objects) != 1:
            return False
        return True

    def execute(self, context):
        me = bpy.context.object.data
        bm = bmesh.new()
        bm.from_mesh(me)

        # store the template mesh in scene prefs
        context.scene.betools_settings.trim_mesh = context.active_object.name
        _settings.trim_slots = _assign_trim_template(bm)
        return {'FINISHED'}


class BETOOLS_OT_TrimFit(bpy.types.Operator):
    """Set a template mesh for trim snapping"""

    bl_idname = "uv.be_trim_fit"
    bl_label = "Trim Fit"
    bl_description = "Snap selected UV shell to a trim"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        if not bpy.context.active_object:
            return False
        if not bpy.context.object.mode == 'EDIT':
            return False
        if context.object.type != 'MESH':
            return False
        if not bpy.context.object.data.uv_layers:
            return False
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        return True

    def execute(self, context):

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        uvs = _uvs.get_selected_uvs(bm, uv_layer)

        template_mesh = bpy.data.objects[context.scene.betools_settings.trim_mesh]
        bm_template = bmesh.new()
        bm_template.from_mesh(template_mesh.data)

        # reassign if it's a new scene
        if not _settings.trim_slots:
            _settings.trim_slots = _assign_trim_template(bm_template)
        
        fit_mode = context.scene.betools_settings.trim_fit_dropdown

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        if len(islands) != 1:
            self.report({'ERROR_INVALID_INPUT'}, "Select only one UV shell!")

        island = islands[0]
        # determine if the shell needs rotated
        island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)
        if island_bounding_box["height"] > island_bounding_box["width"]:
            _uvs.rotate_island(bm, [island], uv_layer, 90.0)

        if fit_mode == 'VERTICAL':
            vertical_snap(bm, uv_layer, uvs, island, island_bounding_box, _settings.trim_slots)
        elif fit_mode == 'HORIZONTAL':
            horizontal_snap(bm, uv_layer, uvs, island, island_bounding_box, _settings.trim_slots)
        elif fit_mode == 'VERTICAL_FIT':
            vertical_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, _settings.trim_slots)
        elif fit_mode == 'HORIZONTAL_FIT':
            horizontal_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, _settings.trim_slots)
        else:
            best_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, _settings.trim_slots)

        bmesh.update_edit_mesh(me)
        return {'FINISHED'}


class BETOOLS_OT_ShiftTrimShell(bpy.types.Operator):
    """Set a template mesh for trim snapping"""

    bl_idname = "uv.be_trim_shift"
    bl_label = "Shift Trim Shell"
    bl_description = "Shift the selected UV shell around the trim template"
    bl_options = {'REGISTER', 'UNDO'}

    direction : EnumProperty(
        name="Direction",
        default="DOWN",
        items=[
            ('UP', "Up", "Shift trim shell up"),
            ('DOWN', "Down", "Shift trim shell down")
        ]
    )

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        if not bpy.context.active_object:
            return False
        if not bpy.context.object.mode == 'EDIT':
            return False
        if context.object.type != 'MESH':
            return False
        if not bpy.context.object.data.uv_layers:
            return False
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        return True

    def execute(self, context):
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        uvs = _uvs.get_selected_uvs(bm, uv_layer)

        template_mesh = bpy.data.objects[context.scene.betools_settings.trim_mesh]
        bm_template = bmesh.new()
        bm_template.from_mesh(template_mesh.data)

        if not _settings.trim_slots:
            _settings.trim_slots = _assign_trim_template(bm_template)

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        if len(islands) != 1:
            self.report({'ERROR_INVALID_INPUT'}, "Select only one UV shell!")

        island = islands[0]
        # determine if the shell needs rotated
        island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

        # get the current 'slot' by testing if the bbox min is in an existing slot
        current_trim_slot = get_selected_island_trim_index(island_bounding_box, _settings.trim_slots)
        direction = -1 if self.direction == 'UP' else 1

        next_trim_slot = current_trim_slot + direction

        if next_trim_slot > len(_settings.trim_slots) - 1:
            next_trim_slot = 0
        elif next_trim_slot < 0:
            next_trim_slot = len(_settings.trim_slots) - 1

        # translate to that slot on the v axis
        # TODO take selected mode into account?

        u_delta = _settings.trim_slots[next_trim_slot]["min"].x - island_bounding_box["min"].x
        v_delta = _settings.trim_slots[next_trim_slot]["min"].y - island_bounding_box["min"].y

        _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)
        return {'FINISHED'}

class BETOOLS_OT_AlignTrimShell(bpy.types.Operator):
    """Set a template mesh for trim snapping"""

    bl_idname = "uv.be_trim_align"
    bl_label = "Align Trim Shell"
    bl_description = "Align the selected UV shell"
    bl_options = {'REGISTER', 'UNDO'}

    mode : EnumProperty(
        name="Mode",
        default='CENTER',
        items=[
            ('LEFT', 'Left', 'Align left'),
            ('CENTER', 'Center', 'Align center'),
            ('RIGHT', 'Right', 'Align right')
        ]
    )

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        if not bpy.context.active_object:
            return False
        if not bpy.context.object.mode == 'EDIT':
            return False
        if context.object.type != 'MESH':
            return False
        if not bpy.context.object.data.uv_layers:
            return False
        if bpy.context.scene.tool_settings.use_uv_select_sync:
            return False
        if bpy.context.area.type != 'IMAGE_EDITOR':
            return False
        return True

    def execute(self, context):

        # TODO get the current trim slot via get_selected_trim_index and use that as the align bounds

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        uvs = _uvs.get_selected_uvs(bm, uv_layer)

        template_mesh = bpy.data.objects[context.scene.betools_settings.trim_mesh]
        bm_template = bmesh.new()
        bm_template.from_mesh(template_mesh.data)

        if not _settings.trim_slots:
            _settings.trim_slots = _assign_trim_template(bm_template)

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        if len(islands) != 1:
            self.report({'ERROR_INVALID_INPUT'}, "Select one UV shell!")
            return {'FINISHED'}

        island = islands[0]
        island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

        # align left = -min.x
        if self.mode == "LEFT":
            u_delta = -island_bounding_box["min"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)
        # align right = 1.0 - max.x
        elif self.mode == 'RIGHT':
            u_delta = 1.0 - island_bounding_box["max"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)
        # align center = .5 - center.x
        else:
            u_delta = .5 - island_bounding_box["center"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)

        return {'FINISHED'}

@_core.edit_mode
def _assign_trim_template(bm):
    bm.transform(bpy.context.object.matrix_world)
    bounding_box = get_mesh_bounding_box(bm)  # min and max for mapping 0-1 uv space
    return _build_trim_faces(bm, bounding_box)

# TODO move this to the mesh module
def get_mesh_bounding_box(bm):
    """ Return the min, max, and span of the bounding box
    """

    bounding_box = {}
    bounds_min = Vector((99999999.0, 99999999.0, 99999999.0))
    bounds_max = Vector((-99999999.0, -99999999.0, -99999999.0))
    bounds_center = Vector((0.0, 0.0, 0.0))

    for vert in bm.verts:

        bounds_min.x = min(bounds_min.x, vert.co.x)
        bounds_min.y = min(bounds_min.y, vert.co.y)
        bounds_min.z = min(bounds_min.z, vert.co.z)

        bounds_max.x = max(bounds_max.x, vert.co.x)
        bounds_max.y = max(bounds_max.y, vert.co.y)
        bounds_max.z = max(bounds_max.z, vert.co.z)

    bounding_box['min'] = bounds_min
    bounding_box['max'] = bounds_max
    bounding_box['width'] = (bounds_max - bounds_min).y
    bounding_box['height'] = (bounds_max - bounds_min).z
    bounding_box['depth'] = (bounds_max - bounds_min).x

    bounds_center.x = (bounds_max - bounds_min).x / 2
    bounds_center.y = (bounds_max - bounds_min).y / 2
    bounds_center.z = (bounds_max - bounds_min).z / 2

    bounding_box['center'] = bounds_center
    bounding_box['area'] = bounding_box['width'] * bounding_box['height'] * bounding_box['depth']
    bounding_box['min_length'] = min(bounding_box['width'], bounding_box['height'], bounding_box['depth'])

    return bounding_box

# TODO move this to the mesh module
def get_face_bounding_box(face):
    bounding_box = {}
    bounds_min = Vector((99999999.0, 99999999.0, 99999999.0))
    bounds_max = Vector((-99999999.0, -99999999.0, -99999999.0))

    for vert in face.verts:
        bounds_min.x = min(bounds_min.x, vert.co.x)
        bounds_min.y = min(bounds_min.y, vert.co.y)
        bounds_min.z = min(bounds_min.z, vert.co.z)
        bounds_max.x = max(bounds_max.x, vert.co.x)
        bounds_max.y = max(bounds_max.y, vert.co.y)
        bounds_max.z = max(bounds_max.z, vert.co.z)

    bounding_box['min'] = bounds_min
    bounding_box['max'] = bounds_max

    return bounding_box

def _build_trim_faces(bm, bounding_box):
    """Sort the faces into a nested array
    """

    face_list = list(bm.faces)
    column = []

    for face in bm.faces:
        column_face = False
        for vert in face.verts:
            # get all verts that match bbox min (enforce x min for now)
            if vert.co.x == bounding_box["min"].x:
                # we have a left most face
                column_face = True
                break
        if column_face:
            column.append(get_face_bounding_box(face))
            face_list.remove(face)

    # sort by max z to build vertical order (3D space)
    sorted_column = sorted(column, key=_sort_max_z, reverse=True)
    column_unsorted_rows = []
    
    # if there are still unsorted faces
    if face_list:
        for row in sorted_column:
            # get the row's height (z) min and max
            # target_bounding_box = get_face_bounding_box(row)
            # turn the row into a list so faces can be added, single faced rows are ok
            temp_row = [row]
            for face in face_list:
                face_bounding_box = get_face_bounding_box(face)
                # look for faces with matching height (z) values
                if face_bounding_box["min"].z == row["min"].z and face_bounding_box["max"].z == row["max"].z:
                    temp_row.append(face_bounding_box)
                    continue
            column_unsorted_rows.append(temp_row)

    column_rows_sorted = column_unsorted_rows

    uv_trim_faces = []
    for row in column_rows_sorted:
        for face_bounds in sorted(row, key=_sort_min_x):
            uv_bounds = face_to_uv_shell(bounding_box, face_bounds)
            print("UV BOUNDS: ")
            pprint(uv_bounds)
            uv_trim_faces.append(uv_bounds)

    return uv_trim_faces

def _sort_max_z(item):
    return item["max"].z

def _sort_min_x(item):
    return item["min"].x

def face_to_uv_shell(mesh_bounding_box, face_bounding_box):
    """Return the UV space representation of the 3D face coordinates.
        Meant for use in trim sheets or other instances where a square 
        plane is mapped to UV space.

    Args:
        bounding_box (dict): Face bounding box where x coords are zero

    Returns:
        dict
    
    """

    if (mesh_bounding_box['max'].y - mesh_bounding_box['min'].y) > _DEPTH_THRESHOLD:
        # TODO raise instead of reporting
        # self.report({'ERROR_INVALID_INPUT'},
        print("BAD TEMPLATE")
        # "It should be on the XZ plane with no Y depth."
        return None

    if (face_bounding_box['max'].y - face_bounding_box['min'].y) > _DEPTH_THRESHOLD:
        # TODO raise instead of reporting
        # self.report({'ERROR_INVALID_INPUT'},
        # "Check your trim template."
        # "It should be on the XZ plane with no Y depth.")
        print("BAD TEMPLATE")
        return None

    # TODO don't need this every time, split out to a different function
    scalar = 1.000000 / (mesh_bounding_box['max'].x - mesh_bounding_box['min'].x)
    x_offset = abs(mesh_bounding_box['min'].x)
    z_offset = abs(mesh_bounding_box['min'].z)

    # coords + min so things will scale correctly
    x_min = (x_offset + face_bounding_box['min'].x) * scalar
    y_min = (z_offset + face_bounding_box['min'].z) * scalar # y in uv space, z in 3D

    x_max = (x_offset + face_bounding_box['max'].x) * scalar
    y_max = (z_offset + face_bounding_box['max'].z) * scalar

    width = x_max - x_min
    height = y_max - y_min
    area = width * height

    # face to uv bounds
    uv_bounds = {
        "min": Vector((x_min, y_min)),
        "max": Vector((x_max, y_max)),
        "width": width,
        "height": height,
        "area": area
    }

    return uv_bounds

def find_matching_trim(bm, island_bounding_box, trim_slots):
    """Find the closest sized trim slot"""

    # width to height ratio
    match = trim_slots[0]
    match_ratio = match["width"] / match["height"]
    island_ratio = island_bounding_box["width"] / island_bounding_box["height"]

    for trim in trim_slots:
        current_slot_ratio = trim["width"] / trim["height"]
        if abs(island_ratio - current_slot_ratio) < abs(island_ratio - match_ratio):
            match = trim
            match_ratio = trim["width"] / trim["height"]
    return match

def get_vertical_scalar(trim_slot, island_bounding_box):
    """Get the scalar needed to fit the uv island to the trim slot"""
    return trim_slot["height"] / island_bounding_box["height"]

def get_horizontal_scalar(trim_slot, island_bounding_box):
    """Get the scalar needed to fit the uv island to the trim slot"""
    return trim_slot["width"] / island_bounding_box["width"]

def vertical_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_slots):
    """Snap the selected island to the nearest vertically sized trim,
        scale to fit verticially.

    Args:
        bm (bmesh)
        island (list): Selected uv island

    """
    # find the best match by width to height ratio
    trim_match = find_matching_trim(bm, island_bounding_box, trim_slots)

    # scale uvs
    vertical_scalar = get_vertical_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, 1.0, vertical_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def horizontal_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_slots):
    """Snap to nearest horizontal sized trim"""

    # find the best match by width to height ratio
    trim_match = find_matching_trim(bm, island_bounding_box, trim_slots)
    horizontal_scalar = get_horizontal_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, horizontal_scalar, 1.0)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def vertical_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_slots):
    """Snap the selected island to the nearest vertically sized trim,
        scale to fit verticially.

    Args:
        bm (bmesh)
        island (list): Selected uv island

    """
    # find the best match by width to height ratio
    trim_match = find_matching_trim(bm, island_bounding_box, trim_slots)

    # scale uvs
    vertical_scalar = get_vertical_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, vertical_scalar, vertical_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def horizontal_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_slots):
    """Snap to nearest horizontal sized trim"""

    # find the best match by width to height ratio
    trim_match = find_matching_trim(bm, island_bounding_box, trim_slots)
    horizontal_scalar = get_horizontal_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, horizontal_scalar, horizontal_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def best_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_slots):
    """Scale to the best fit trim"""

    # find the best match by width to height ratio
    trim_match = find_matching_trim(bm, island_bounding_box, trim_slots)
    horizontal_scalar = get_horizontal_scalar(trim_match, island_bounding_box)
    vertical_scalar = get_vertical_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, horizontal_scalar, vertical_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def get_selected_island_trim_index(island_bounding_box, sorted_trim_slots):
    """Get the index based on the trim slots"""

    for i, trim in enumerate(sorted_trim_slots):
        if island_bounding_box["min"].x >= trim["min"].x and island_bounding_box["min"].x < trim["max"].x:
            if island_bounding_box["min"].y >= trim["min"].y and island_bounding_box["min"].y < trim["max"].y:
                return i
    return -1

def get_next_island_trim_index(current_index, direction, trim_slots):
    """Get the next trim slot"""
    trim_slots = sorted(trim_slots, key=lambda d:d["min"].x)

    if current_index + direction < 0:
        current_index = len(trim_slots) - 1
    elif current_index + direction > len(trim_slots) - 1:
        current_index = 0
    else:
        current_index += direction

    new_slot = {
        "trim": trim_slots[current_index],
        "index": current_index
    }
    return new_slot


bpy.utils.register_class(BETOOLS_OT_AssignTrimTemplate)
bpy.utils.register_class(BETOOLS_OT_TrimFit)
bpy.utils.register_class(BETOOLS_OT_ShiftTrimShell)
bpy.utils.register_class(BETOOLS_OT_AlignTrimShell)
