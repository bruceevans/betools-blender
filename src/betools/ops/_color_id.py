
import bpy
import bmesh
from bpy.props import IntProperty

from ..utils import _uvs
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
        settings.color_id_count += 1

        if settings.color_id_count > 15:
            self.report({"WARNING"}, "Reached the maximum number of colors!")
            return {'FINISHED'}

        # get the name from settings

        """
        material ={
            "name": settings.material_name,
            "color": (.1, .2, .7),  # random color or pick from list
            "index": settings.color_id_count,
            "rename": False,
            "material": ""
        }
        """
        # settings.id_colors.append(material)

        # set the appropriate settings
        setattr(settings, "color_id_{}_name".format(settings.color_id_count - 1), settings.material_name)

        # reset
        settings.material_name = "New Color"

        return {'FINISHED'}


class BETOOLS_OT_RemoveColor(bpy.types.Operator):
    bl_idname = "uv.be_remove_color"
    bl_label = "Remove Color for ID Map"
    bl_description = "Remove a color from the ID bake"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # if context.scene.betools_settings.id_colors:
            # del context.scene.betools_settings.id_colors[len(context.scene.betools_settings.id_colors)-1]
        
        settings = context.scene.betools_settings
        if settings.color_id_count > 0:
            settings.color_id_count -= 1

        return {'FINISHED'}


class BETOOLS_OT_EnableRename(bpy.types.Operator):
    bl_idname = "uv.be_enable_rename_color"
    bl_label = "Enable Rename Color"
    bl_description = "Enable rename color ID material"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(
        name="Index"
    )

    def execute(self, context):
        settings = context.scene.betools_settings
        setattr(settings, "color_id_{}_rename".format(self.index), True)
        return {'FINISHED'}


class BETOOLS_OT_RenameID(bpy.types.Operator):
    bl_idname = "uv.be_rename_color"
    bl_label = "Rename Color"
    bl_description = "Rename color ID material"
    bl_options = {'REGISTER', 'UNDO'}

    index : bpy.props.IntProperty(
        name="Index"
    )

    def execute(self, context):
        settings = context.scene.betools_settings
        setattr(settings, "color_id_{}_name".format(self.index), settings.rename_material)
        settings.rename_material = "New Color"
        setattr(settings, "color_id_{}_rename".format(self.index), False)
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
        settings = context.scene.betools_settings
        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()
        uvs = _uvs.get_selected_uvs(bm, uv_layer)
        if not uvs:
            self.report({'ERROR_INVALID_INPUT'}, "Select some UVs!")

        # modify the color to match
        color = tuple(getattr(settings, "color_id_{}".format(self.index))) + (1.0,)
        material_name = "BE_ID_{}".format(getattr(settings, "color_id_{}_name".format(self.index)))
        
        mat = bpy.data.materials.new(name=material_name)
        mat.use_nodes=True
        mat.node_tree.nodes["Principled BSDF"].inputs[0].default_value = color
        obj.data.materials.append(mat)

        # get material index
        mat_index = len(obj.data.materials) - 1
        bpy.context.object.active_material_index = mat_index
        
        _uvs.store_selection()

        # assign to selected faces via selected uvs
        for face in bm.faces:
            if face.select:
                count = 0
                for loop in face.loops:
                    if loop[uv_layer].select:
                        count+=1
                if not count == len(face.loops):
                    face.select = False

        # assign to selected faces
        bpy.ops.object.material_slot_assign()

        _uvs.restore_selection()
        bmesh.update_edit_mesh(me)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        #Only in Edit mode
        if bpy.context.active_object.mode != 'EDIT':
            return False
        #Requires UV map
        if not bpy.context.object.data.uv_layers:
            return False
        return True


class BETOOLS_OT_BakeID(bpy.types.Operator):
    bl_idname = "uv.be_bake_id"
    bl_label = "Bake ID Map"
    bl_description = "Use cycles to bake a color ID map"
    bl_options = {'REGISTER', 'UNDO'}

    margin : bpy.props.IntProperty(
        name="Index"
    )

    size : bpy.props.IntProperty(
        name='Size',
        default=2048
    )

    def execute(self, context):

        obj = bpy.context.active_object
        # create the ID Map based on current map size or use existing map
        image = bpy.data.images.new("Color_ID", width=self.size, height=self.size)
        image.use_fake_user = True

        # add it to the materials as a image texture node
        for mat in obj.data.materials:
            nodes = mat.node_tree.nodes
            node = nodes.new('ShaderNodeTexImage')
            node.image = image

        renderer = context.scene.render.engine
        if renderer != 'CYCLES':
            context.scene.render.engine = 'CYCLES'
        # diffuse bake mode - color only
        context.scene.cycles.bake_type = 'DIFFUSE'
        bpy.context.scene.render.bake.use_pass_direct = False
        bpy.context.scene.render.bake.use_pass_indirect = False
        bpy.context.scene.render.bake.use_pass_color = True
        bpy.context.scene.render.bake.margin = self.margin
        # select object (object mode?)
        previous_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        # run bake
        bpy.ops.object.bake('INVOKE_DEFAULT', type='DIFFUSE')
        # reset
        context.scene.render.engine = renderer
        bpy.ops.object.mode_set(mode=previous_mode)

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if not bpy.context.active_object:
            return False
        return True


class BETOOLS_OT_ClearIDMats(bpy.types.Operator):
    bl_idname = "uv.be_clear_id_mats"
    bl_label = "Clear ID Mats"
    bl_description = "Remove all the materials created from the ID bake"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        # get the object's mats
        previous_mode = bpy.context.object.mode
        bpy.ops.object.mode_set(mode='OBJECT')
        obj = bpy.context.active_object
        for idx, mat in enumerate(obj.data.materials):
            context.object.active_material_index = idx
            if mat:
                if mat.name.startswith("BE_ID"):
                    bpy.ops.object.material_slot_remove()
                    bpy.data.materials.remove(mat)
        bpy.ops.object.mode_set(mode=previous_mode)

        return {'FINISHED'}


bpy.utils.register_class(BETOOLS_OT_AddColor)
bpy.utils.register_class(BETOOLS_OT_RemoveColor)
bpy.utils.register_class(BETOOLS_OT_EnableRename)
bpy.utils.register_class(BETOOLS_OT_RenameID)
bpy.utils.register_class(BETOOLS_OT_AssignColor)
bpy.utils.register_class(BETOOLS_OT_BakeID)
bpy.utils.register_class(BETOOLS_OT_ClearIDMats)
