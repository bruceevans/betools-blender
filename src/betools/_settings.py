# TODO choose game engine (ue4, unity, hide)

import bpy
import bmesh
import operator

from . utils import _constants

edit_pivot_mode = False
uv_selection_mode = ''
uv_loops_selection = []
uv_pivot_selection = ''
uv_pivot_selection_position = (0, 0)

selection_mode = (False, False, True)
vert_selection = []     # indices
face_selection = []      # indices

game_engine = ''        # Unreal or Unity or Source?

uv_map_rename_mode = False

id_colors = []

def set_uv_map_dropdown(self, context, index):
    if bpy.context.active_object != None:
        if bpy.context.active_object.type == 'MESH':
            if bpy.context.object.data.uv_layers:
                bpy.context.object.data.uv_layers[index].active_render = True
                get_uv_maps(self, context)
                bpy.context.scene.betools_settings.uv_maps = str(index)

def on_uv_map_dropdown(self, context):
    if bpy.context.active_object != None:
        if bpy.context.active_object.type == 'MESH':
            if bpy.context.object.data.uv_layers:
                index = int(bpy.context.scene.betools_settings.uv_maps)
                if index < len(bpy.context.object.data.uv_layers):
                    bpy.context.object.data.uv_layers.active_index = index
                    bpy.context.object.data.uv_layers[index].active_render = True

def get_uv_maps(self, context):
    if bpy.context.active_object == None:
        return[]
    if bpy.context.active_object.type != 'MESH':
        return[]
    if not bpy.context.object.data.uv_layers:
        return []
    maps = []
    count = 0
    for uv_loop in bpy.context.object.data.uv_layers:
        maps.append((str(count), uv_loop.name, "Switching to {}".format(uv_loop.name), count))
        count += 1
    return maps

class BETOOLSProperties(bpy.types.PropertyGroup):

    translate_u : bpy.props.FloatProperty(name='U')
    translate_v : bpy.props.FloatProperty(name='V')

    scale_u : bpy.props.FloatProperty(name='U', default=1.0)
    scale_v : bpy.props.FloatProperty(name='V', default=1.0)

    angle : bpy.props.IntProperty(name='Angle')

    random_translate : bpy.props.FloatProperty(name='rand_translate')
    random_scale : bpy.props.FloatProperty(name='rand_scale')
    random_rotate : bpy.props.FloatProperty(name='rand_rotate')

    sort_padding : bpy.props.FloatProperty(name='Pad', default=0.01)
    pack_padding : bpy.props.FloatProperty(name='Pad', default=0.01)

    current_texel_density : bpy.props.FloatProperty(name='Texel Density', default=256.0)
    texel_density : bpy.props.FloatProperty(name='Texel Density', default=256.0)
    
    texel_density_units : bpy.props.StringProperty(name='Texel Density Units', default="Centimeters")
    image_size : bpy.props.IntProperty(name='Image Size')

    material_name : bpy.props.StringProperty(name='Material Name', default='New Color')

    map_size_dropdown : bpy.props.EnumProperty(
        items = _constants.MAP_SIZES,
		name = "Texture Map Size",
        default = '1024'
	)

    checker_map_dropdown : bpy.props.EnumProperty(
        items = _constants.CHECKER_MAPS,
		name = "Checker Maps",
        default = 'CHECKER'
	)

    uv_maps : bpy.props.EnumProperty(
        items = get_uv_maps,
		name = "UV Maps",
        update = on_uv_map_dropdown
	)

    uv_map_new_name : bpy.props.StringProperty(name='Rename UV Map', default = 'New UV Map')

    # TODO checkbox pref for auto rotate on sort

bpy.utils.register_class(BETOOLSProperties)