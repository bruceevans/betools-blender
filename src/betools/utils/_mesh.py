#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh
from mathutils import Vector

def getFaceCenter():
    """ Get the center position of the selected face

        args:
            face (face?)

        returns:
            pos (Vec3)
            normal (Vec3)
    """

    bm = get_mesh()
    if not bm:
        return (None, None)
    faces = [face for face in bm.faces if face.select]
    if not len(faces) == 1:
        return (None, None)
    return faces[0].calc_center_median_weighted(), faces[0].normal

def get_mesh():
    """ Small helper to get the current bmesh in edit mode
    """
    
    ob = bpy.context.active_object
    
    if not ob.mode == 'EDIT':
        print("Must be in EDIT mode when getting a BMESH object")
        return
    
    return bmesh.from_edit_mesh(ob.data)

def getSelectedVerts():
    bm = get_mesh()
    return [vert for vert in bm.verts if vert.select]

def getSelectedEdges():
    bm = get_mesh()
    return [edge for edge in bm.edges if edge.select]

def getSelectedFaces():
    """ The data gets destroyed, try global?
    """
    bm = get_mesh()
    return [face for face in bm.faces if face.select]

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

def rotateToCoordinates(obj, direction):

    bpy.ops.object.select_all(action='DESELECT')
    bpy.data.objects[obj].select_set(True)

    bpy.data.objects[obj].rotation_mode = 'QUATERNION'
    bpy.data.objects[obj].rotation_quaternion = direction.to_track_quat('X','Z')

def translateToCoordinates(objectLocation, targetLocation):
    """ Translate object to a target coordinate location

        args:
            objectLocation (vec3)
            targetLocation (vec3)
    """
    delta = mathutils.Vector(targetLocation - objectLocation)
    bpy.ops.transform.translate(value=delta)