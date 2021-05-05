#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from .. import _settings


class CenterPivot(bpy.types.Operator):
    bl_label = "Center Pivot"
    bl_description = "Move the pivot point to the center of the object."
    bl_idname = "mesh.be_center_pivot"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if _settings.edit_pivot_mode:
            return False
        return True


class Pivot2Cursor(bpy.types.Operator):
    bl_label = "Pivot to 3D Cursor"
    bl_description = "Move the pivot point to the 3D cursor"
    bl_idname = "mesh.be_pivot2cursor"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if _settings.edit_pivot_mode:
            return False
        return True


# TODO Double check this, maybe use a toggle button and log to show you're in edit pivot mode
class EditPivot(bpy.types.Operator):
    bl_label = "Edit Pivot"
    bl_description = "Edit the object's pivot"
    bl_idname = "mesh.be_editpivot"
    bl_options = {'REGISTER', 'UNDO'}

    def createPivot(self, context, obj):
        self.report({'INFO'}, 'IN EDIT PIVOT MODE. SET THE PIVOT AND CLICK EDIT PIVOT AGAIN')
        bpy.ops.object.empty_add(type='ARROWS', location=obj.location)
        pivot = bpy.context.active_object
        pivot.name = obj.name + ".PivotHelper"
        pivot.location = obj.location
        _settings.edit_pivot_mode = True

    def getPivot(self, context, obj):
        pivot = obj.name + ".PivotHelper"
        if bpy.data.objects.get(pivot) is None:
            return False
        else:
            bpy.data.objects[obj.name].select_set(False)
            bpy.data.objects[pivot].select_set(True)
            context.view_layer.objects.active = bpy.data.objects[pivot]
            return True

    def applyPivot(self, context, pivot):
        obj = bpy.data.objects[pivot.name[:-12]]
        piv_loc = pivot.location
        #I need to create piv as it seem like the pivot location is passed by reference? Still no idea why this happens
        cl = context.scene.cursor.location
        piv = (cl[0],cl[1],cl[2])
        context.scene.cursor.location = piv_loc
        bpy.context.view_layer.objects.active = obj
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='MEDIAN')
        context.scene.cursor.location = (piv[0],piv[1],piv[2])
        #Select pivot, delete it and select obj again
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[pivot.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        context.view_layer.objects.active = obj
        _settings.edit_pivot_mode = False
        
    def execute(self, context):
        obj = bpy.context.active_object
        if  obj.name.endswith(".PivotHelper"):
            self.applyPivot(context, obj)
        elif self.getPivot(context, obj):
            piv = bpy.context.active_object
        else:
            self.createPivot(context,obj)
        return{'FINISHED'}


bpy.utils.register_class(CenterPivot)
bpy.utils.register_class(Pivot2Cursor)
bpy.utils.register_class(EditPivot)
