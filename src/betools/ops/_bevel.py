#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class SmartBevel(bpy.types.Operator):
    bl_idname = "mesh.be_bevel"
    bl_label = "Smart Bevel"
    bl_description = "Bevel Edges or Chamfer Vertices"
    bl_options = {'REGISTER', 'UNDO'}

    def bevel(self):
        selection_mode = (tuple(bpy.context.scene.tool_settings.mesh_select_mode))
        if selection_mode[0]:
            bpy.ops.mesh.bevel('INVOKE_DEFAULT',affect='VERTICES')
        elif selection_mode[1]:
            bpy.ops.mesh.bevel('INVOKE_DEFAULT',affect='EDGES')
        else:
            pass

    def execute(self, context):
        self.bevel()
        return{"FINISHED"}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if not bpy.context.active_object.mode == 'EDIT':
            return False
        return True

bpy.utils.register_class(SmartBevel)
