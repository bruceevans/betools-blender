
import bpy

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

        return {'FINISHED'}


bpy.utils.register_class(BETOOLS_OT_AddColor)
