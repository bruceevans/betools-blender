
import bpy
import bmesh
import operator

import time
import math

from mathutils import Vector
from collections import defaultdict

from ..utils import _ui
from .. import _settings

from pprint import pprint


#######################################
# UV Selections - uvs, faces, islands #
#######################################


def store_selection():
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    uv_layers = bm.loops.layers.uv.verify()

    # store mode to settings
    _settings.uv_selection_mode = bpy.context.scene.tool_settings.uv_select_mode
    _settings.uv_pivot_selection = bpy.context.space_data.pivot_point
    _settings.uv_pivot_selection_position = bpy.context.space_data.cursor_location.copy()

    # mesh selection (store indices)
    _settings.selection_mode = tuple(bpy.context.scene.tool_setting.mesh_select_mode)
    _settings.vert_selection = [ vert.index for vert in bm.verts if vert.select ]
    _settings.face_selection = [ face.index for face in bm.faces if face.select ]
    _settings.uv_loops_selection = []

    for face in bm.faces:
        for loop in face.loops:
            if loop[uv_layers].select:
                _settings.uv_loops_selection.append( [face.index, loop.vert.index] )

def restore_selection(bm = None, uv_layers = None):
    if bpy.context.object.mode != 'EDIT':
        bpy.ops.object.mode_set(mode = 'EDIT')

    if not bm:
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    if not uv_layers:
        uv_layers = bm.loops.layers.uv.verify()

    bpy.context.scene.tool_settings.uv_select_mode = _settings.uv_selection_mode
    bpy.context.space_data.pivot_point = _settings.uv_pivot_selection

    uvView = _ui.GetUVView()
    if uvView:
        bpy.ops.uv.cursor_set(uvView, location=_settings.uv_pivot_selection_position)

    bpy.ops.mesh.select_all(action='DESELECT')

    if hasattr(bm.verts, "ensure_lookup_table"): 
        bm.verts.ensure_lookup_table()
        bm.faces.ensure_lookup_table()

    # faces
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    for i in _settings.face_selection:
        if i < len(bm.verts):
            bm.faces[i].select = True

    # verts
    bpy.ops.mesh.select_mode(use_extend=False, use_expand=False, type='FACE')
    for i in _settings.vert_selection:
        if i < len(bm.verts):
            bm.verts[i].select = True

    # restore selection mode
    bpy.context.scene.tool_settings.mesh_select_mode = _settings.selection_mode

    # uv face selection
    bpy.ops.uv.select_all(uvView, action = 'DESELECT')
    for uvs in _settings.uv_loops_selection:
        for loop in bm.faces[uvs[0]].loops:
            if loop.vert.index == uvs[1]:
                loop[uv_layers].select = True
                break

    bpy.context.view_layer.update()

def get_selected_faces():
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    faces = [ face for face in bm.faces if face.select ]
    return faces

def set_selected_faces(faces):
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    uv_layers = bm.loops.layers.uv.verify()
    for face in faces:
        for loop in face.loops:
            loop[uv_layers].select = True

def get_selected_uv_edges(bm, uv_layers):
    """
    uv_edges = []
    for face in bm.faces:
        uv_edge = []  # temp, only append if it doesn't already exist
        for loop in face.loops:
            if loop[uv_layers].select:
                if loop[uv_layers].uv not in uv_edge:
                    uv_edge.append(loop[uv_layers].uv)
                    # pprint(loop[uv_layers].uv)
                else:
                    print("Already have that uv")
            # loop is an edge face is a collection of loops
            if len(uv_edge) <= 1:
                continue
            if uv_edge not in uv_edges and reversed(uv_edge) not in uv_edges:
                uv_edges.append(uv_edge)
            else:
                print("Already have that edge")
    pprint(uv_edges)
    return uv_edges
    """
    faces = []
    for face in bm.faces:
        for loop in face.loops:
            if loop[uv_layers].select:
                faces.append(face)
                break
    
    # get the edges in each face
    uv_edges = []
    for face in faces:
        uv_edge = []
        for loop in face.loops:
            if loop[uv_layers].select:

                # how many connections are selected
                con_next = loop.link_loop_next
                con_prev = loop.link_loop_prev

                if con_next[uv_layers].select and not con_prev[uv_layers].select:
                    uv_edge.append(loop[uv_layers])
                    uv_edge.append(con_next[uv_layers])
                    if uv_edge not in uv_edges:
                        uv_edges.append(uv_edge)
                    break
                elif not con_next[uv_layers].select and con_prev[uv_layers].select:
                    # prepend con_prev, break
                    uv_edge.append(con_prev[uv_layers])
                    uv_edge.append(loop[uv_layers])
                    if uv_edge not in uv_edges:
                        uv_edges.append(uv_edge)
                    break
                else:
                    # both are selected, make two edges and append both
                    uv_edge.append(loop[uv_layers])
                    uv_edge.append(con_next[uv_layers])
                    if uv_edge not in uv_edges:
                        uv_edges.append(uv_edge)

                    uv_edge.clear()

                    uv_edge.append(con_prev[uv_layers])
                    uv_edge.append(loop[uv_layers])
                    if uv_edge not in uv_edges:
                        uv_edges.append(uv_edge)
                    break

    # Will return duplicates currently
    # TODO optimize
    return uv_edges

def get_uvs_from_verts(bm, uv_layers):
    vert_uv = {}
    for face in bm.faces:
        for loop in face.loops:
            vert = loop.vert
            uv = loop[uv_layers]
            if vert not in vert_uv:
                vert_uv[vert] = [uv]
            else:
                vert_uv[vert].append(uv)
    return vert_uv

# uvs from edges TODO

def get_uvs_from_faces(bm, uv_layers):
    
    """ Face to uvs
    """

    uvs = []
    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                if loop[uv_layers].select:
                    uvs.append( loop[uv_layers] )
    return uvs

def get_verts_from_uvs(bm, uv_layers):
    """ Get mesh verts from uvs
    """
    verts = set()
    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                if loop[uv_layers].select:
                    verts.add(loop.vert)
    return list(verts)

def get_edges_from_uvs(bm, uv_layers):
    """ Mesh edges from uvs
    """
    verts = get_verts_from_uvs(bm, uv_layers)
    edges = [ edge for edge in bm.edges if edge.verts[0] in verts and edge.verts[1] in verts ]
    return edges

def get_faces_from_uvs(bm, uv_layers):
    """ Mesh faces from uvs
    """
    faces = []
    for face in bm.faces:
        if face.select:
            count = 0
            for loop in face.loops:
                if loop[uv_layers].select:
                    count+=1
            if count == len(face.loops):
                faces.append(face)
    return faces

def get_uv_layer(ops_obj, bm):
    # get UV layer
    if not bm.loops.layers.uv:
        ops_obj.report({'WARNING'},
                        "Object must have more than one UV map")
        return None
    uv_layer = bm.loops.layers.uv.verify()
    return uv_layer

def get_selection_bounding_box():
    # TODO makes sure this is getting every island
    # islands and mesh as args?
    bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
    uv_layers = bm.loops.layers.uv.verify()

    bounding_box = {}

    boundsMin = Vector((99999999.0,99999999.0))
    boundsMax = Vector((-99999999.0,-99999999.0))
    boundsCenter = Vector((0.0,0.0))

    selection = False

    # for island in islands:

    for face in bm.faces:
        if face.select:
            for loop in face.loops:
                if loop[uv_layers].select:
                    selection = True
                    uv = loop[uv_layers].uv
                    boundsMin.x = min(boundsMin.x, uv.x)
                    boundsMin.y = min(boundsMin.y, uv.y)
                    boundsMax.x = max(boundsMax.x, uv.x)
                    boundsMax.y = max(boundsMax.y, uv.y)

    if not selection:
        return None

    bounding_box['min'] = boundsMin
    bounding_box['max'] = boundsMax
    bounding_box['width'] = (boundsMax - boundsMin).x
    bounding_box['height'] = (boundsMax - boundsMin).y

    boundsCenter.x = (boundsMax.x + boundsMin.x)/2
    boundsCenter.y = (boundsMax.y + boundsMin.y)/2

    bounding_box['center'] = boundsCenter
    bounding_box['area'] = bounding_box['width'] * bounding_box['height']
    bounding_box['minLength'] = min(bounding_box['width'], bounding_box['height'])

    return bounding_box

def get_selected_islands(bm = None, uv_layers = None):
    if not bm:
        bm = bmesh.from_edit_mesh(bpy.context.active_object.data)
        uv_layers = bm.loops.layers.uv.verify()
    
    if bpy.context.scene.tool_settings.use_uv_select_sync == False:
        bpy.ops.uv.select_linked()

    # selected_faces = [ face for face in bm.faces if face.select and face.loops[0][uv_layers].select ]
    selected_faces = []
    for face in bm.faces:
        if face.select and face.loops[0][uv_layers].select:
            selected_faces.append(face)

    unparsed_faces = selected_faces.copy()
    islands = []

    for face in selected_faces:
        if face in unparsed_faces:
            # select face
            bpy.ops.uv.select_all(action='DESELECT')
            face.loops[0][uv_layers].select = True
            bpy.ops.uv.select_linked()

            islandFaces = [face]
            for wholeFace in unparsed_faces:
                if wholeFace != face and wholeFace.select and wholeFace.loops[0][uv_layers].select:
                    islandFaces.append(wholeFace)
            
            for wholeFace in islandFaces:
                unparsed_faces.remove(wholeFace)

            islands.append(islandFaces)

    # reselect
    for face in selected_faces:
        for loop in face.loops:
            loop[uv_layers].select = True

    return islands


#######################################
#  UV Transforms                      #
#######################################

def translate_island(mesh, island, uv_layer, deltaX, deltaY):
    """ Translate uv islands in UV space

        args:
            mesh: obj data (bpy.context.active_object.data)
            island (list) : uv island
            uv_layer
            deltaX (float)
            deltaY (float)

    """

    # adjust uv coordinates
    for face in island:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            loop_uv.uv[0] += deltaX
            loop_uv.uv[1] += deltaY

    bmesh.update_edit_mesh(mesh)

def scale_island(mesh, island, uv_layer, scaleU, scaleV):
    """ scale """

    # translate to 0, 0 (bbox center?)

    for face in island:
        for loop in face.loops:
            loop_uv = loop[uv_layer]
            loop_uv.uv[0] *= scaleU
            loop_uv.uv[1] *= scaleV

    bmesh.update_edit_mesh(mesh)

def rotate_island(mesh, islands, uv_layer, angle):
    """ rotate """
    cos_theta, sin_theta = math.cos(math.radians(-angle)), math.sin(math.radians(-angle))
    
    # rotate pivot still a little off TODO
    bounding_box = get_selection_bounding_box()

    center = (bounding_box.get("max") - bounding_box.get("min"))/2
    box_max = bounding_box.get("max")

    pivot = box_max - center
    for island in islands:
        for face in island:
            for loop in face.loops:
                loop_uv = loop[uv_layer]

                loop_uv.uv[0] -= pivot.x
                loop_uv.uv[1] -= pivot.y

                duR = loop_uv.uv[0] * cos_theta - loop_uv.uv[1] * sin_theta
                dvR = loop_uv.uv[0] * sin_theta + loop_uv.uv[1] * cos_theta

                loop_uv.uv[0] = duR + pivot.x
                loop_uv.uv[1] = dvR + pivot.y

    bmesh.update_edit_mesh(mesh)
            

class UVTransformProperties(bpy.types.PropertyGroup):

    translate_u : bpy.props.FloatProperty(name='U')
    translate_v : bpy.props.FloatProperty(name='V')

    scale_u : bpy.props.FloatProperty(name='U', default=1.0)
    scale_v : bpy.props.FloatProperty(name='V', default=1.0)

    angle : bpy.props.IntProperty(name='Angle')

bpy.utils.register_class(UVTransformProperties)


#######################################
#  Helpers                            #
#######################################
