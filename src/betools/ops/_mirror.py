#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from bpy.props import EnumProperty
from .. import _settings

from ..utils import _constants

# TODO update to take a property
_AXIS = {
    'X':(True, False, False),
    'Y':(False, True, False),
    'Z':(False, False, True)
}

class SmartMirror(bpy.types.Operator):
    bl_label = "Mirror"
    bl_description = "Mirror in a given direction"
    bl_idname = "mesh.smart_mirror"
    bl_options = {'REGISTER', 'UNDO'}

    direction : EnumProperty(
        name="Direction",
        default='X',
        items = [
            ('X', 'X', 'Mirror the object in the X direction'),
            ('Y', 'Y', 'Mirror the object in the Y direction'),
            ('Z', 'Z', 'Mirror the object in the Z direction')
        ]
    )

    def execute(self, context):
        bpy.ops.object.mode_set(mode = 'OBJECT')
        bpy.ops.object.duplicate()
        # bpy.ops.transform.mirror(orient_type='GLOBAL', orient_matrix=((1, 0, 0), (0, 1, 0), (0, 0, 1)), orient_matrix_type='GLOBAL', constraint_axis=(False, False, True))

        bpy.ops.transform.mirror(
            orient_type='GLOBAL',
            constraint_axis=(_AXIS.get(self.direction)),
            # proportional_size=1,
            # use_proportional_connected=False,
            # use_proportional_projected=False
            )
        bpy.ops.object.transform_apply(location=False, rotation=False, scale=True)

        bpy.ops.object.editmode_toggle()
        bpy.ops.mesh.select_mode(type='FACE')
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.normals_make_consistent(inside=False)
        bpy.ops.object.editmode_toggle()
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if _settings.edit_pivot_mode:
            return False
        if context.object.type != 'MESH':
            return False
        if context.object is None:
            return False
        return True


bpy.utils.register_class(SmartMirror)
