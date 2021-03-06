#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import os
import bpy
import bmesh
import math
from bpy.props import EnumProperty, FloatVectorProperty, FloatProperty
from mathutils import Vector
from ..utils import _uvs
from ..utils import _constants


_UNITS = {
    "Centimeters" : 0.01,
    "Meters" : 1.00,
    "Feet" : 3.28084,
    "Yards" : 1.09361
}


class BETOOLS_OT_GetTexel(bpy.types.Operator):
    bl_idname = "uv.be_get_texel"
    bl_label = "Get Texel Density"
    bl_description = "Get the texel density of the selected UV island"
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if len(bpy.context.selected_objects) > 1:
            return False
        return True

    def execute(self, context):

        if _uvs.get_current_image() is None:
            self.report({'ERROR_INVALID_INPUT'}, "Select or create an image!")
            return {'FINISHED'}

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        current_texture = _uvs.get_current_image()
        islands = _uvs.get_selected_islands(bm, uv_layer)

        if not islands:
            self.report({'ERROR_INVALID_INPUT'}, "Select a UV island!")
            return {'FINISHED'}

        texel_density = get_texel_density(self, context, current_texture, bm, uv_layer)
        if not texel_density:
            return {'FINISHED'}

        context.scene.betools_settings.texel_density = texel_density
        return {'FINISHED'}


class BETOOLS_OT_SetTexel(bpy.types.Operator):
    bl_idname = "uv.be_set_texel"
    bl_label = "Set Texel Density"
    bl_description = "Set the texel density of the selected UV island"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        if _uvs.get_current_image() is None:
            self.report({'ERROR_INVALID_INPUT'}, "Select or create an image!")
            return {'FINISHED'}

        obj = bpy.context.active_object
        me = obj.data
        bm = bmesh.from_edit_mesh(me)
        uv_layer = bm.loops.layers.uv.verify()

        current_texture = _uvs.get_current_image()
        texel_density = context.scene.betools_settings.texel_density
        if not texel_density:
            return {'FINISHED'}
            
        set_texel_density(self, context, current_texture, bm, me, uv_layer, texel_density)
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        if len(bpy.context.selected_objects) > 1:
            return False
        if context.scene.tool_settings.use_uv_select_sync:
            return False
        return True


class BETOOLS_OT_CubeHelper(bpy.types.Operator):
    bl_idname = "uv.be_cube_helper"
    bl_label = "Cube Helper"
    bl_description = "Create a unit cube to visualize texel density"
    bl_options = {'REGISTER', 'UNDO'}

    size : EnumProperty (
        name = "Cube Size",
        default = "1M",
        items = [
            ('.5M', '.5m', 'Half meter'),
            ('1M', '1m', 'One meter'),
            ('2M', '2m', 'Two meters'),
            ('4M', '4m', 'Four meters')
        ]
    )

    def execute(self, context):

        file_path = os.path.join(_constants.MDL_FOLDER, 'unit-cube.blend')
        inner_path = 'Object'
        object_name = 'unit-cube-{}'.format(self.size)

        if not os.path.isfile(file_path):
            return {'FINISHED'}

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, object_name),
            directory=os.path.join(file_path, inner_path),
            filename=object_name
        )

        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if bpy.context.object.mode != 'OBJECT':
            return False
        return True

    
class BETOOLS_OT_CreateImage(bpy.types.Operator):
    bl_idname = "uv.be_create_image"
    bl_label = "Create Image"
    bl_description = "Create an image for the UV editor"
    bl_options = {'REGISTER', 'UNDO'}

    size : bpy.props.IntProperty(
        name='Size',
        default=2048
    )

    def execute(self, context):
        image = bpy.data.images.new("BT_Image", width=self.size, height=self.size)
        bpy.context.area.spaces.active.image = image
        return {'FINISHED'}


class BETOOLS_OT_AssignMat(bpy.types.Operator):
    bl_idname = "uv.be_assign_mat"
    bl_label = "Assign Material"
    bl_description = "Assign a preset checker map at a given size"
    bl_options = {'REGISTER', 'UNDO'}

    size : bpy.props.IntProperty(
        name='Size',
        default=2048
    )

    def execute(self, context):

        original_mode = bpy.context.object.mode

        if bpy.context.object.mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')

        selected_objects = [obj for obj in bpy.context.selected_objects]
        if not selected_objects:
            self.report({'ERROR_INVALID_INPUT'}, "Select a mesh")
            return {'FINISHED'}

        file_path = os.path.join(_constants.MDL_FOLDER, 'materials.blend')
        if not os.path.isfile(file_path):
            self.report({'WARNING'}, "Resources are missing from BE Tools! Reinstall the addon.")
            return {'FINISHED'}
        inner_path = 'Material'

        size = _constants.MATERIAL_SIZES.get(str(self.size))
        selected_map = context.scene.betools_settings.checker_map_dropdown.capitalize()  # lower case the enum
        material_name ='BT_{}_{}'.format(selected_map, size)

        for mat in bpy.data.materials:
            if mat.name == material_name:
                material = bpy.data.materials.get(material_name)
                for obj in selected_objects:
                    obj.select_set(True)
                    assign_material(obj, material)
                return {'FINISHED'}

        bpy.ops.wm.append(
            filepath=os.path.join(file_path, inner_path, material_name),
            directory=os.path.join(file_path, inner_path),
            filename=material_name
        )

        # Assign material
        for obj in selected_objects:
            obj.select_set(True)
            material = bpy.data.materials.get(material_name)
            assign_material(obj, material)

        bpy.ops.object.mode_set(mode = original_mode)

        return {'FINISHED'}


def assign_material(obj, mat):
    if obj.data.materials:
        obj.data.materials[0] = mat
    else:
        obj.data.materials.append(mat)

    image = None

    nodes = mat.node_tree.nodes
    for node in nodes:
        if node.type == 'TEX_IMAGE':
            image = node.image
            break

    if image:
        # open in image editor
        bpy.context.area.spaces.active.image = image


def get_texel_density(op, context, uv_image, bm, uv_layer):

    mesh_faces = get_selected_object_faces()
    if not mesh_faces:
        op.report({'ERROR_INVALID_INPUT'}, "Select a mesh")
        return None

    uv_sum = 0
    vert_sum = 0

    islands = _uvs.get_selected_islands(bm, uv_layer)
    if len(islands) != 1:
        op.report({'ERROR_INVALID_INPUT'}, "Select ONE uv island when measuring texel density!")
        return None

    for face in islands[0]:
        uv_tri = [loop[uv_layer].uv for loop in face.loops]
        vert_tri = [vert.co for vert in face.verts]

        uv_area = _uvs.get_area_triangle_uv(
            uv_tri[0], uv_tri[1], uv_tri[2],
            uv_image.size[0], uv_image.size[1])

        face_area = _uvs.get_area_triangle(
            vert_tri[0], vert_tri[1], vert_tri[2]
        )

        uv_sum += math.sqrt(uv_area) * min(uv_image.size[0], uv_image.size[1])
        vert_sum += math.sqrt(face_area)
        
    if uv_sum == 0 or vert_sum == 0:
        return 0.00
    else:
        return uv_sum / vert_sum

def set_texel_density(op, context, uv_image, bm, me, uv_layer, density):
    """
    """

    islands = _uvs.get_selected_islands(bm, uv_layer)

    for island in islands:
        uv_sum = 0
        vert_sum = 0
        for face in island:
            uv_tri = [loop[uv_layer].uv for loop in face.loops]
            vert_tri = [vert.co for vert in face.verts]

            uv_area = _uvs.get_area_triangle_uv(
            uv_tri[0], uv_tri[1], uv_tri[2],
            uv_image.size[0], uv_image.size[1])

            face_area = _uvs.get_area_triangle(
                vert_tri[0], vert_tri[1], vert_tri[2]
            )

            uv_sum += math.sqrt(uv_area) * min(uv_image.size[0], uv_image.size[1])
            vert_sum += math.sqrt(face_area)

        scale = 0
        if density > 0 and uv_sum > 0 and vert_sum > 0:
            scale = density / (uv_sum / vert_sum)

        _uvs.scale_island(me, island, uv_layer, scale, scale)

def get_selected_object_faces():
	object_faces_indices = {}

	previous_mode = bpy.context.object.mode

	if bpy.context.object.mode == 'EDIT':
		# Only selected Mesh faces
		obj = bpy.context.active_object
		if obj.type == 'MESH' and obj.data.uv_layers:
			bm = bmesh.from_edit_mesh(obj.data)
			bm.faces.ensure_lookup_table()
			object_faces_indices[obj] = [face.index for face in bm.faces if face.select]
	else:
		# Selected objects with all faces each
		selected_objects = [obj for obj in bpy.context.selected_objects]
		for obj in selected_objects:
			if obj.type == 'MESH' and obj.data.uv_layers:
				bpy.ops.object.mode_set(mode='OBJECT')
				bpy.ops.object.select_all(action='DESELECT')
				bpy.context.view_layer.objects.active = obj
				obj.select_set( state = True, view_layer = None)

				bpy.ops.object.mode_set(mode='EDIT')
				bm = bmesh.from_edit_mesh(obj.data)
				bm.faces.ensure_lookup_table()
				object_faces_indices[obj] = [face.index for face in bm.faces]

	bpy.ops.object.mode_set(mode=previous_mode)

	return object_faces_indices

bpy.utils.register_class(BETOOLS_OT_GetTexel)
bpy.utils.register_class(BETOOLS_OT_SetTexel)
bpy.utils.register_class(BETOOLS_OT_CubeHelper)
bpy.utils.register_class(BETOOLS_OT_CreateImage)
bpy.utils.register_class(BETOOLS_OT_AssignMat)
