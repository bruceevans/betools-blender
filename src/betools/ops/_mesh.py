#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh

import math
import mathutils


class BETOOLS_OT_RecalcNormals(bpy.types.Operator):
    bl_idname = "mesh.be_recalc_normals"
    bl_label = "Recalculate Normals"
    bl_description = "Recalculate exterior normals, must be in EDIT mode with FACE selection"
    bl_options = {'REGISTER', 'UNDO'}

    def consistentNormals(self):
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)

    def execute(self, context):

        if bpy.context.active_object.mode == 'OBJECT':
            bpy.ops.object.editmode_toggle()
            self.consistentNormals()
            bpy.ops.object.editmode_toggle()
        else:
            self.consistentNormals()
        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True


class BETOOLS_OT_SnapToFace(bpy.types.Operator):
    bl_idname = "mesh.be_snap_to_face"
    bl_label = "Snap to Face"
    bl_description = "Snap mesh to selected face"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        
        targetTransform, targetRotation = getFaceCenter()

        if not targetTransform or bpy.context.object.mode == 'OBJECT':
            self.report({'INFO'}, 'Switch to FACE mode and select a face to snap.')
            return {"FINISHED"}

        bpy.ops.object.mode_set(mode='OBJECT')

        faceObject = bpy.context.selected_objects[0]
        targetTransform += faceObject.location
        
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[context.scene.snapObject].select_set(True)

        if faceObject == bpy.data.objects[context.scene.snapObject]:
            self.report({'INFO'}, 'Invalid selection! Choose a different object to snap.')
            return {"FINISHED"}

        location = bpy.data.objects[context.scene.snapObject].location
        translateToCoordinates(location, targetTransform)
        rotateToCoordinates(context.scene.snapObject, targetRotation)

        return {"FINISHED"}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if not bpy.types.Scene.snapObject:
            return False
        return True


################################################
#   Utilities
################################################

def getFaceCenter():
    """ Get the center position of the selected face

        args:
            face (face?)

        returns:
            pos (Vec3)
            normal (Vec3)
    """

    bm = getMesh()
    if not bm:
        return (None, None)
    faces = [face for face in bm.faces if face.select]
    if not len(faces) == 1:
        return (None, None)
    return faces[0].calc_center_median_weighted(), faces[0].normal

def getMesh():
    """ Small helper to get the current bmesh in edit mode
    """
    
    ob = bpy.context.active_object
    
    if not ob.mode == 'EDIT':
        print("Must be in EDIT mode when getting a BMESH object")
        return
    
    return bmesh.from_edit_mesh(ob.data)

def getSelectedVerts():
    bm = getMesh()
    return [vert for vert in bm.verts if vert.select]

def getSelectedEdges():
    bm = getMesh()
    return [edge for edge in bm.edges if edge.select]

def getSelectedFaces():
    """ The data gets destroyed, try global?
    """
    bm = getMesh()
    return [face for face in bm.faces if face.select]

def getMeshBoundingBox(mesh):
    """ Return the min, max, and span of the bounding box
    """

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


bpy.utils.register_class(BETOOLS_OT_RecalcNormals)
bpy.utils.register_class(BETOOLS_OT_SnapToFace)
