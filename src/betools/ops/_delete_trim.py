import bpy
import bmesh
from mathutils import Vector
from pprint import pprint


# TODO for full version, if not in 'EDIT' mode, save mode, run the op, switch back to mode
# maybe create a decorator for that?

# Now you have all the faces from the mesh, 
# When a user selects a uv shell and choose trim snap or whatever,
# iter throught the face and find the nearest size vert or hor (Depending on selection)
# scale the correct axis to fit the mesh face (converted to UV space, 0-1 x,y)
# snap based on the selected anchor point

def _assign_trim_template():
    selected_object = bpy.context.active_object
    if not selected_object:
        return
    if not selected_object.type == 'MESH':
        return
    bm = bmesh.from_edit_mesh(selected_object.data)
    bm.transform(bpy.context.object.matrix_world)
    bounding_box =  get_mesh_bounding_box(bm)  # min and max for mapping 0-1 uv space

    trim_faces = _build_trim_faces(bm, bounding_box)
        
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

def _remap_bounds(bounding_box):
    """Remap the bounding box to UV space, meant for planes/trims
    """

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
            column.append(face)

    sorted_faces = []
    if len(column) < len(bm.faces):
        leftover_faces = list(set(face_list) - set(column))
        for row in column:
            # get the row's height (z) min and max
            target_bounding_box = get_face_bounding_box(row)
            # turn the row into a list so faces can be added, single faced rows are ok
            temp_row = [row]
            for face in leftover_faces:
                face_bounding_box = get_face_bounding_box(face)
                # look for faces with matching height (z) values
                if face_bounding_box["min"].z == target_bounding_box["min"].z and face_bounding_box["max"].z == target_bounding_box["max"].z:
                    temp_row.append(face)
                    continue
            sorted_faces.append(row)
    return sorted_faces

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

_assign_trim_template()
