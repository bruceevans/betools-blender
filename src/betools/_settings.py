# TODO choose game engine (ue4, unity, hide)

import bpy
import bmesh
import operator

edit_pivot_mode = False
uv_selection_mode = ''
uv_loops_selection = []
uv_pivot_selection = ''
uv_pivot_selection_position = (0, 0)

selection_mode = (False, False, True)
vert_selection = []     # indices
face_selection = []      # indices

game_engine = ''        # Unreal or Unity


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
    
    # TODO Enum prop?
    texel_density_units : bpy.props.StringProperty(name='Texel Density Units', default="Centimeters")
    image_size : bpy.props.IntProperty(name='Image Size')
    
    # TODO checkbox for auto rotate on sort

bpy.utils.register_class(BETOOLSProperties)