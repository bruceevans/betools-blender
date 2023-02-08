#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
from mathutils import Vector
from bpy.props import EnumProperty
from ..utils import _uvs
from ..utils import _mesh
from ..utils import mode
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
        if not _settings.trim_slots:
            self.report(
                {'ERROR_INVALID_INPUT'},
                "Invalid  template!"
                "It should be on the XZ plane with no Y depth.")
            return {'FINISHED'}
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
            self.report({'ERROR_INVALID_INPUT'}, "Select one UV shell!")
            return {'FINISHED'}

        island = islands[0]
        # determine if the shell needs rotated
        island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)
        if island_bounding_box["height"] > island_bounding_box["width"]:
            _uvs.rotate_island(bm, [island], uv_layer, 90.0)
        trim_match = find_matching_trim(bm, island_bounding_box, _settings.trim_slots)
        if fit_mode == 'VERTICAL':
            vertical_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'HORIZONTAL':
            horizontal_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'VERTICAL_FIT':
            vertical_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'HORIZONTAL_FIT':
            horizontal_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        else:
            best_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
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

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        if len(islands) != 1:
            self.report({'ERROR_INVALID_INPUT'}, "Select one UV shell!")
            return {'FINISHED'}

        fit_mode = context.scene.betools_settings.trim_fit_dropdown

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

        trim_match = _settings.trim_slots[next_trim_slot]

        if fit_mode == 'VERTICAL':
            vertical_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'HORIZONTAL':
            horizontal_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'VERTICAL_FIT':
            vertical_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        elif fit_mode == 'HORIZONTAL_FIT':
            horizontal_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)
        else:
            best_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match)

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

        current_trim_slot = get_selected_island_trim_index(island_bounding_box, _settings.trim_slots)
        trim_slot = _settings.trim_slots[current_trim_slot]

        # align left = -min.x
        if self.mode == "LEFT":
            u_delta = trim_slot["min"].x - island_bounding_box["min"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)
        # align right = 1.0 - max.x
        elif self.mode == 'RIGHT':
            u_delta = trim_slot["max"].x - island_bounding_box["max"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)
        # align center = .5 - center.x
        else:
            u_delta = trim_slot["center"].x - island_bounding_box["center"].x
            _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, 0.0)

        return {'FINISHED'}

@mode.edit_mode
def _assign_trim_template(template_mesh):

    template_mesh.transform(bpy.context.object.matrix_world)
    bounding_box = _mesh.get_mesh_bounding_box(template_mesh)  # min and max for mapping 0-1 uv space

    # print("Bounding box: ")
    # print(bounding_box)

    # TODO get a sorted flat list
    # TODO round to the near something float
    # TODO after flat list sorted by y (z) then work on row sorting
   
    face_list = list(template_mesh.faces)
    # column = []

    face_bounding_boxes = []

    for face in template_mesh.faces:
        face_bounding_boxes.append(_mesh.get_face_bounding_box(face))

        """
        for vert in face.verts:
            # get all verts that match bbox min (enforce x min for now)
            # if vert.co.x == bounding_box["min"].x:
            if vert.co.x == bounding_box["min"].x:
                # we have a left most face
                face_bounding_boxes.append(_mesh.get_face_bounding_box(face))
                face_list.remove(face)
                # column_face = True  # should be row face NOTE
                break
        """

    # sort by max z to build vertical order (3D space)
    sorted_bounds = sorted(face_bounding_boxes, key=_sort_max_z, reverse=True)
    
    """
    column_unsorted_rows = []

    # if there are still unsorted faces
    for row in sorted_column:
        # get the row's height (z) min and max
        # target_bounding_box = get_face_bounding_box(row)
        # turn the row into a list so faces can be added, single faced rows are ok
        temp_row = [row]
        for face in face_list:
            face_bounding_box = _mesh.get_face_bounding_box(face)
            # look for faces with matching height (z) values
            if face_bounding_box["min"].z == row["min"].z and face_bounding_box["max"].z == row["max"].z:
                temp_row.append(face_bounding_box)
                continue
        column_unsorted_rows.append(temp_row)

    column_rows_sorted = column_unsorted_rows

    uv_trim_faces = []
    for row in column_rows_sorted:
        for face_bounds in sorted(row, key=_sort_min_z):
            uv_bounds = face_to_uv_shell(bounding_box, face_bounds)
            if not uv_bounds:
                # invalid input
                return None
            uv_trim_faces.append(uv_bounds)
    """

    uv_trim_faces = []

    for face_bounds in sorted_bounds:
        uv_bounds = face_to_uv_shell(bounding_box, face_bounds)
        if not uv_bounds:
            continue
        uv_trim_faces.append(uv_bounds)

    print(len(uv_trim_faces))

    return uv_trim_faces

def _sort_max_z(item):
    return item["max"].z

def _sort_min_x(item):
    return item["min"].x

def _sort_min_z(item):
    return item["min"].z

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
        return None

    if (face_bounding_box['max'].y - face_bounding_box['min'].y) > _DEPTH_THRESHOLD:
        return None

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
    center = Vector((x_min + width/2.0, y_min + width/2.0))

    # face to uv bounds
    uv_bounds = {
        "min": Vector((x_min, y_min)),
        "max": Vector((x_max, y_max)),
        "width": width,
        "height": height,
        "area": area,
        "center": center
    }

    return uv_bounds

def find_matching_trim(bm, island_bounding_box, trim_slots):
    """Find the closest sized trim slot"""

    if not trim_slots:
        print("No trim slots assigned!")
        return

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

def vertical_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match):
    """Snap the selected island to the nearest vertically sized trim,
        scale to fit verticially.

    Args:
        bm (bmesh)
        island (list): Selected uv island

    """

    # scale uvs
    vertical_scalar = get_vertical_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, 1.0, vertical_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def horizontal_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match):
    """Snap to nearest horizontal sized trim"""

    horizontal_scalar = get_horizontal_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, horizontal_scalar, 1.0)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def vertical_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match):
    """Snap the selected island to the nearest vertically sized trim,
        scale to fit verticially.

    Args:
        bm (bmesh)
        island (list): Selected uv island

    """

    # scale uvs
    vertical_scalar = get_vertical_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, vertical_scalar, vertical_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def horizontal_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match):
    """Snap to nearest horizontal sized trim"""

    horizontal_scalar = get_horizontal_scalar(trim_match, island_bounding_box)
    _uvs.scale_uvs(bm, uv_layer, uvs, horizontal_scalar, horizontal_scalar)

    # update the scaled bbox
    island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)

    # translate
    u_delta = trim_match["min"].x - island_bounding_box["min"].x
    v_delta = trim_match["min"].y - island_bounding_box["min"].y
    _uvs.translate_uvs(bm, uv_layer, uvs, u_delta, v_delta)

def best_fit_snap(bm, uv_layer, uvs, island, island_bounding_box, trim_match):
    """Scale to the best fit trim"""

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
