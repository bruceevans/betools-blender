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
vert_selection = [] # indices
face_selection = [] # indices

uv_map_rename_mode = False

previous_unit = ''

##############################################################################
##############################################################################

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
        maps.append((str(count), uv_loop.name, "UV Map: {}".format(uv_loop.name), count))
        count += 1
    return maps

def show_uv_stretch(self, context):
    if bpy.context.space_data.uv_editor.show_stretch:
        bpy.context.space_data.uv_editor.show_stretch = False
    else:
        bpy.context.space_data.uv_editor.show_stretch = True

def uv_stretch_type(self, context):
    bpy.context.space_data.uv_editor.display_stretch_type = context.scene.betools_settings.uv_stretch_type

def get_color():

    return bpy.props.FloatVectorProperty(
        name="Color",
        description="Set Color for ID",
        subtype="COLOR",
        default=(.1, .2, .8),
        size=3,
        max=1.0, min=0.0
    )

def get_name():
    return bpy.props.StringProperty(
        name="Color ID Name",
        default = "New Color"
    )

def get_rename():
    return bpy.props.BoolProperty(
        name = "Rename ID Color",
        default = False
    )

def update_units(self, context):
    settings = context.scene.betools_settings
    if settings.unit == 'METERS' or settings.unit == 'CENTIMETERS':
        bpy.context.scene.unit_settings.system = 'METRIC'
    else:
        bpy.context.scene.unit_settings.system = 'IMPERIAL'
    bpy.context.scene.unit_settings.length_unit = settings.unit


##############################################################################
##############################################################################


class BETOOLSProperties(bpy.types.PropertyGroup):

    # ADDON PREFERENCES

    quick_export_path : bpy.props.StringProperty(
        name='Quick OBJ Export',
        description='Choose a directory:',
        default='',
        maxlen=1024,
        subtype='DIR_PATH')

    game_engine : bpy.props.EnumProperty(
        items = [
            ('UNREAL', 'Unreal Engine 4', 'Presets for Unreal Engine 4'),
            ('UNITY', 'Unity', 'Presets for Unity'),
            ('SOURCE', 'Source', 'Presets for the Source SDK'),
            ('GODOT', 'Godot', 'Presets for Godot')
        ],
        name = "Game Engine Presets",
        description='Choose your game engine. Best to pick this at the start of a project.'
    )

    unit : bpy.props.EnumProperty(
        items = [
            ('CENTIMETERS', 'Centimeters', 'Centimeters for unit measurement'),
            ('METERS', 'Meters', 'Meters for unit measurement'),
            ('INCHES', 'Inches', 'Inches for unit measurement'),
            ('FEET', 'Feet', 'Feet for unit measurement')
        ],
        name = "Units"
        # update=update_units
    )

    # TOOL PROPERTIES

    snapping : bpy.props.BoolProperty(
        name='Snapping',
        default=False
    )

    translate_u : bpy.props.FloatProperty(name='U')
    translate_v : bpy.props.FloatProperty(name='V')

    scale_u : bpy.props.FloatProperty(name='U', default=1.0)
    scale_v : bpy.props.FloatProperty(name='V', default=1.0)

    angle : bpy.props.IntProperty(name='Angle')

    random_translate : bpy.props.FloatProperty(name='rand_translate')
    random_scale : bpy.props.FloatProperty(name='rand_scale')
    random_rotate : bpy.props.FloatProperty(name='rand_rotate')

    sort_padding : bpy.props.FloatProperty(name='Pad', default=0.01)
    padding : bpy.props.IntProperty(
        name='Padding',
        description='UV pixel padding',
        default=8,
        min=0,
        max=64)

    relax_iterations : bpy.props.IntProperty(
        name="Relaxe Iterations (hundreds)",
        default=4,
        min=0,
        max=50)

    current_texel_density : bpy.props.FloatProperty(name='Texel Density', default=256.0)
    texel_density : bpy.props.FloatProperty(name='Texel Density', default=256.0)
    
    texel_density_units : bpy.props.StringProperty(name='Texel Density Units', default="Centimeters")
    image_size : bpy.props.IntProperty(
        name='Image Size',
        description='UV Texture Size',
        default=1024,
        min=0,
        max=8192)

    material_name : bpy.props.StringProperty(name='New Color', default='New Color')
    rename_material : bpy.props.StringProperty(name='Rename Color', default='New Color')

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

    color_id_count : bpy.props.IntProperty(
        name="Color ID Count",
        default = 0,
        min=0,
        max=15)

    color_id_pixel_bleed : bpy.props.IntProperty(
        name="Bleed",
        default = 8)

    color_id_0 : get_color()
    color_id_0_name : get_name()
    color_id_0_rename : get_rename()

    color_id_1 : get_color()
    color_id_1_name : get_name()
    color_id_1_rename : get_rename()

    color_id_2 : get_color()
    color_id_2_name : get_name()
    color_id_2_rename : get_rename()

    color_id_3 : get_color()
    color_id_3_name : get_name()
    color_id_3_rename : get_rename()

    color_id_4 : get_color()
    color_id_4_name : get_name()
    color_id_4_rename : get_rename()

    color_id_5 : get_color()
    color_id_5_name : get_name()
    color_id_5_rename : get_rename()

    color_id_6 : get_color()
    color_id_6_name : get_name()
    color_id_6_rename : get_rename()

    color_id_7 : get_color()
    color_id_7_name : get_name()
    color_id_7_rename : get_rename()

    color_id_8 : get_color()
    color_id_8_name : get_name()
    color_id_8_rename : get_rename()

    color_id_9 : get_color()
    color_id_9_name : get_name()
    color_id_9_rename : get_rename()

    color_id_10 : get_color()
    color_id_10_name : get_name()
    color_id_10_rename : get_rename()

    color_id_11 : get_color()
    color_id_11_name : get_name()
    color_id_11_rename : get_rename()

    color_id_12 : get_color()
    color_id_12_name : get_name()
    color_id_12_rename : get_rename()

    color_id_13 : get_color()
    color_id_13_name : get_name()
    color_id_13_rename : get_rename()

    color_id_14 : get_color()
    color_id_14_name : get_name()
    color_id_14_rename : get_rename()

    color_id_15 : get_color()
    color_id_15_name : get_name()
    color_id_15_rename : get_rename()

    show_uv_stretch : bpy.props.BoolProperty(
        name = "UV Stretch",
        default = False,
        update = show_uv_stretch
    )

    uv_stretch_type : bpy.props.EnumProperty(
        items = [
            ('ANGLE', 'Angle', ''),
            ('AREA', 'Area', '')
        ],
        name = "UV Stretch Type",
        update = uv_stretch_type
    )

    uv_maps : bpy.props.EnumProperty(
        items = get_uv_maps,
		name = "UV Maps",
        update = on_uv_map_dropdown
	)

    uv_map_new_name : bpy.props.StringProperty(name='Rename UV Map', default = 'New UV Map')
