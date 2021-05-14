#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy


class BETOOLS_OT_VertSnap(bpy.types.Operator):
    bl_idname = "mesh.be_vert_snap"
    bl_label = "Vert Snapping"
    bl_description = "Snap to vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.tool_settings.snap_elements = {'VERTEX'}
        context.scene.tool_settings.snap_target = 'CENTER'
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


class BETOOLS_OT_VertSnapClosest(bpy.types.Operator):
    bl_idname = "mesh.be_closest_vert_snap"
    bl_label = "Closest Vert Snapping"
    bl_description = "Snap to closest vertex"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.tool_settings.snap_elements = {'VERTEX'}
        context.scene.tool_settings.snap_target = 'CLOSEST'
        return {'FINISHED'}
    
    @classmethod
    def poll(cls, context):
        return True


class BETOOLS_OT_GridSnap(bpy.types.Operator):
    bl_idname = "mesh.be_grid_snap"
    bl_label = "Grid Snapping"
    bl_description = "Snap to grid"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        context.scene.tool_settings.snap_elements = {'INCREMENT'}
        context.scene.tool_settings.use_snap_grid_absolute = True
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        return True


bpy.utils.register_class(BETOOLS_OT_VertSnap)
bpy.utils.register_class(BETOOLS_OT_VertSnapClosest)
bpy.utils.register_class(BETOOLS_OT_GridSnap)
