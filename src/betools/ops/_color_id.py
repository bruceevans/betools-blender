
import bpy
from bpy.props import IntProperty
from .. import _settings

# color ID ops


"""
basically, there's an add button, you click add and select a color,
choose your faces and apply

4-5 colors per row so it doesn't get too crazy

1. Add buton
2. Color row (max 4 colrs)
    - Color bar (picker)
    - Apply button

"""

class BETOOLS_OT_AddColor(bpy.types.Operator):
    bl_idname = "uv.be_add_color"
    bl_label = "Add Color for ID Map"
    bl_description = "Add a color to use in a color ID map bake"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        settings = context.scene.betools_settings

        if len(_settings.id_colors) > 15:
            self.report({"WARNING"}, "Reached the maximum number of colors!")
            return {'FINISHED'}

        # get the name from settings
        material ={
            "name": settings.material_name,
            "color": (.1, .2, .7),
            "index": len(_settings.id_colors)
        }
        _settings.id_colors.append(material)
        settings.material_name = ""
        return {'FINISHED'}


class BETOOLS_OT_RemoveColor(bpy.types.Operator):
    bl_idname = "uv.be_remove_color"
    bl_label = "Remove Color for ID Map"
    bl_description = "Remove a color from the ID bake"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(
        name="Index"
    )

    def execute(self, context):
        del _settings.id_colors[self.index]

        # TODO remember colors

        """
        settings = context.scene.betools_settings
        for i in range(len(_settings.id_colors)):
            setattr(settings, "color_id_{}".format(i), _settings.id_colors[i].get("color")) # not being set
        """
        return {'FINISHED'}

    
class BETOOLS_OT_AssignColor(bpy.types.Operator):
    bl_idname = "uv.be_assign_color"
    bl_label = "Assign Color"
    bl_description = "Assign color to selected uvs"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(
        name="Index"
    )

    def execute(self, context):

        return {'FINISHED'}


class BETOOLS_OT_BakeID(bpy.types.Operator):
    bl_idname = "uv.be_bake_id"
    bl_label = "Bake ID Map"
    bl_description = "Use cycles to bake a color ID map"
    bl_options = {'REGISTER', 'UNDO'}

    bleed : bpy.props.IntProperty(
        name="Index"
    )

    def execute(self, context):

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if not _settings.id_colors:
            return False
        return True

bpy.utils.register_class(BETOOLS_OT_AddColor)
bpy.utils.register_class(BETOOLS_OT_RemoveColor)
bpy.utils.register_class(BETOOLS_OT_AssignColor)
bpy.utils.register_class(BETOOLS_OT_BakeID)
