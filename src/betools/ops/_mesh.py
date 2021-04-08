#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class RecalcNormals(bpy.types.Operator):
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


def getMeshBoundingBox():
    """ Return the min, max, and span of the bounding box
    """

bpy.utils.register_class(RecalcNormals)
