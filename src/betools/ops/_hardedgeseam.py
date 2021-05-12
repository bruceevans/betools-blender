#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class SeamHardEdge(bpy.types.Operator):
    bl_label = "Hard Edge Seams"
    bl_description = "Create seams along hard edges based on Auto-Smooth angle. Must be in EDIT mode with EDGE select activated"
    bl_idname = "mesh.seams_from_hard_edge"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self):
        self.current_selection = bpy.context.object.data

    def make_seams(self):
        if not self.current_selection.use_auto_smooth:
            self.report({'INFO'}, 'Turn on auto smooth')
        else:
            bpy.ops.object.mode_set(mode = 'EDIT')
            smooth_angle = bpy.context.object.data.auto_smooth_angle
            bpy.ops.mesh.select_all(action ='DESELECT')
            bpy.ops.mesh.edges_select_sharp(sharpness=smooth_angle)
            bpy.ops.mesh.mark_seam(clear=False)
            bpy.context.active_object.select_set(False)

    def execute(self, context):
        self.make_seams()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        sm = tuple(bpy.context.tool_settings.mesh_select_mode)
        if not sm[1]:
            return False
        if context.object is None:
            return False
        if not bpy.context.active_object.mode == 'EDIT':
            return False
        return True

bpy.utils.register_class(SeamHardEdge)
