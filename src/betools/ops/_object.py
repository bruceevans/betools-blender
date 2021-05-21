#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
import bmesh

from ..utils import _constants
from mathutils import Vector
from bpy.props import FloatProperty

# resize all objects in the scene
class BETOOLS_OT_ResizeObjects(bpy.types.Operator):
    bl_idname = "mesh.be_resize_objects"
    bl_label = "Resize Objects"
    bl_description = "Attempt to resize all objects in the scene."
    bl_options = {"REGISTER"}

    @classmethod
    def poll(cls, context):
        return True

    def execute(self, context):
        settings = context.scene.betools_settings

        objects = context.scene.objects
        objects_to_scale = []

        for obj in objects:
            if obj.type == 'ARMATURE':
                self.report({'WARNING'}, "Armature in the scene! Can't rescale objects")
                return({'FINISHED'})
            if obj.scale != Vector((1.0, 1.0, 1.0)):
                self.report({'WARNING'}, "Apply scale to {} before resizing".format(obj.name))
                return({'FINISHED'})
            objects_to_scale.append(obj)

        target_unit = _constants.UNITS.get(settings.unit.capitalize())
        current_unit = _constants.UNITS.get(context.scene.unit_settings.length_unit.capitalize())
        scalar = target_unit / current_unit

        scale_value = (scalar, scalar, scalar)

        if settings.unit != context.scene.unit_settings.length_unit:
            if settings.unit == 'METERS' or settings.unit == 'CENTIMETERS':
                context.scene.unit_settings.system = 'METRIC'
            else:
                context.scene.unit_settings.system = 'IMPERIAL'
            context.scene.unit_settings.length_unit = settings.unit

        for obj in objects_to_scale:
            # translate to origin
            obj.select_set(True)
            delta = (obj.location)*scalar
            obj.location = (0, 0, 0)
            obj.scale = scale_value
            obj.location = delta
            # apply scale
            bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)
            obj.select_set(False)

        return {"FINISHED"}


class BETOOLS_OT_ChangeUnit(bpy.types.Operator):
    bl_idname = "mesh.be_change_units"
    bl_label = "Change Units"
    bl_description = "Change the project units."
    bl_options = {"REGISTER"}

    def execute(self, context):
        settings = context.scene.betools_settings
        if settings.unit != context.scene.unit_settings.length_unit:
            if settings.unit == 'METERS' or settings.unit == 'CENTIMETERS':
                context.scene.unit_settings.system = 'METRIC'
            else:
                context.scene.unit_settings.system = 'IMPERIAL'
            context.scene.unit_settings.length_unit = settings.unit
        return {"FINISHED"}


bpy.utils.register_class(BETOOLS_OT_ResizeObjects)
bpy.utils.register_class(BETOOLS_OT_ChangeUnit)
