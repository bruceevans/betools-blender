#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import math
import bpy
import bmesh
from bpy.props import EnumProperty
from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
from mathutils import Vector
from ..utils import _uvs
from ..utils import _core
from .. import _settings
from .. import _constants


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
        return True

    def execute(self, context):
        me = bpy.context.object.data
        # TODO assign the mesh to a property so it can be stored with the scene
        bm = bmesh.new()
        bm.from_mesh(me)

        # trim slots contains rows of trims/faces in the form
        # of bounding box min/max vectors
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
        
        fit_mode = context.scene.betools_settings.trim_fit_dropdown
        
        if not _settings.trim_slots:
            # TODO raise
            print("SELECT A TRIM TEMPLATE")
            return {'FINISHED'}

        obj = context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        trim_slots = _settings.trim_slots

        """
        # TODO move this to the assign temlate function -----

        mesh_bounding_box = get_mesh_bounding_box(bm)

        uv_trim_faces = []
        for row in trim_slots:
            for face_bounds in row:
                uv_trim_faces.append(face_to_uv_shell(mesh_bounding_box, face_bounds))

        # ----------------------------------------------------
        """

        _uvs.store_selection()
        islands = _uvs.get_selected_islands(bm, uv_layer)
        _uvs.restore_selection(bm, uv_layer)

        if len(islands) != 1:
            # TODO raise
            print("SELECT ONLY ONE ISLAND")
            return {'FINISHED'}

        island = islands[0]
        # determine if the shell needs rotated
        # get island bounding box
        island_bounding_box = _uvs.get_island_bounding_box(island, uv_layer)
        if island_bounding_box["height"] > island_bounding_box["width"]:
            _uvs.rotate_island(bm, [island], uv_layer, 90.0)

        # TODO snap based on mode

        if fit_mode == 'VERTICAL':
            print("MATCHING TO NEAREST VERTICAL SIZE")
        elif fit_mode == 'HORIZONTAL':
            print("MATCHING TO NEAREST HORIZONTAL SIZE")
        elif fit_mode == 'VERTICAL_FIT':
            print("SCALING ENTIRE UV SHELL TO MATCH NEAREST VERTICAL SIZE")
        elif fit_mode == 'HORIZONTAL_FIT':
            print("SCALING ENTIRE SHELL FOR HORIZONTAL FIT")
        else:
            print("SCALING WIDTH AND HEIGHT SEPARATELY TO FIT THE NEAREST SIZE")

        # for each mesh face, get the uv coords


        return {'FINISHED'}


class BETOOLS_OT_ShiftTrimShell(bpy.types.Operator):
    """Set a template mesh for trim snapping"""

    bl_idname = "uv.be_trim_shift"
    bl_label = "Shift Trim Shell"
    bl_description = "Shift the selected UV shell around the trim template"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # passthrough currently
        return {'FINISHED'}

@_core.edit_mode
def _assign_trim_template(bm):
    bm.transform(bpy.context.object.matrix_world)
    bounding_box =  get_mesh_bounding_box(bm)  # min and max for mapping 0-1 uv space
    return _build_trim_faces(bm, bounding_box)
        
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

    # TODO make it into a more organize list of dicts
    # min, max, width, height, area, center

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

    sorted_faces = []
    if face_list:
        for row in column:
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
            sorted_faces.append(temp_row)

    uv_trim_faces = []
    for row in sorted_faces:
        for face_bounds in row:
            uv_trim_faces.append(face_to_uv_shell(bounding_box, face_bounds))
    return uv_trim_faces

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
    # if mesh_bounding_box['min'].y != mesh_bounding_box['max'].y:
        # TODO raise
        print("INVALID TRIM MESH")
        return None

    if (face_bounding_box['max'].y - face_bounding_box['min'].y) > _DEPTH_THRESHOLD:
    # if face_bounding_box['min'].y != face_bounding_box['max'].y:
        # TODO raise
        print("INVALID TRIM MESH")
        return None

    # TODO don't need this every time, split out to a different function
    scalar = 1.000000 / (mesh_bounding_box['max'].x - mesh_bounding_box['min'].x)
    print("SCALAR: ")
    print(scalar)
    x_offset = abs(mesh_bounding_box['min'].x)
    z_offset = abs(mesh_bounding_box['min'].z)

    # coords + min so things will scale correctly
    x_min = (x_offset + face_bounding_box['min'].x) * scalar
    y_min = (z_offset + face_bounding_box['min'].z) * scalar # y in uv space, z in 3D

    x_max = (x_offset + face_bounding_box['max'].x) * scalar
    y_max = (z_offset + face_bounding_box['max'].z) * scalar

    # face to uv bounds
    uv_bounds = {
        "min": Vector((x_min, y_min)),
        "max": Vector((x_max, y_max))
    }

    return uv_bounds


bpy.utils.register_class(BETOOLS_OT_AssignTrimTemplate)
bpy.utils.register_class(BETOOLS_OT_TrimFit)
bpy.utils.register_class(BETOOLS_OT_ShiftTrimShell)
