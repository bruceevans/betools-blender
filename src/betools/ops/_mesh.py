#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh


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

    def _getFaceTarget(self):
        bm = getMesh()
        targetFace =[face for face in bm.faces if face.select][0]
        return targetFace.calc_center_median_weighted(), targetFace.normal

    def execute(self, context):
        
        # snapObject = bpy.types.Scene.snapObject
        transform, rotation = self._getFaceTarget()

        # switch to object mode

        # select snap object

        print("SNAP OBJECT")
        print(context.scene.snapObject)
        bpy.ops.object.mode_set(mode='OBJECT')
        # deselect objects
        bpy.ops.object.select_all(action='DESELECT')
        bpy.data.objects[context.scene.snapObject].select_set(True)

        # TODO
        # transform deltas
        # rotation deltas

        bpy.ops.transform.translate(value=transform)
        bpy.ops.transform.rotate(value=rotation.x, orient_axis='X')
        bpy.ops.transform.rotate(value=rotation.y, orient_axis='Y')
        bpy.ops.transform.rotate(value=rotation.z, orient_axis='Z')

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

def getMesh():
    """ Small helper to get the current bmesh in edit mode
    """
    
    ob = bpy.context.active_object
    
    if not ob.mode == 'EDIT':
        print("Must be in EDIT mode when to get a BMESH object")
        return
    
    return bmesh.from_edit_mesh(ob.data)

def getSelectedVerts():
    pass

def getSelectedEdges():
    pass

def getSelectedFaces():
    """ The data gets destroyed, try global?
    """
    bm = getMesh()
    return [face for face in bm.faces if face.select]

def getFaceCenter(face):
    """ Get the center position of the selected face

        args:
            face (face?)

        returns:
            pos (Vec3)
    """

    bm = getMesh()
    faces = [face for face in bm.faces if face.select]
    if not len(faces) == 1:
        print("Select a single face!")
        return
    return faces[0].calc_center_median_weighted()

def getMeshBoundingBox(mesh):
    """ Return the min, max, and span of the bounding box
    """

bpy.utils.register_class(BETOOLS_OT_RecalcNormals)
bpy.utils.register_class(BETOOLS_OT_SnapToFace)
