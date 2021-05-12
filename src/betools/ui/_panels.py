#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import os
from math import radians

import bpy

import bpy.utils.previews
from bpy.types import Menu
from bpy.types import Panel

from .. ops import *
from .. utils import _icon
from .. utils import _constants
from .. _settings import BETOOLSProperties
from .. import _settings

from bpy.props import StringProperty, FloatProperty, IntProperty, PointerProperty


class BEPreferencesPanel(bpy.types.AddonPreferences):
    """ Preferences for the addon, found in the edit menu
    """

    bl_idname = 'betools'  # this needs to be the name of the main addon module

    game_engine : bpy.props.EnumProperty(
        items = [
			('UE4', 'Unreal Engine 4', 'Unreal Engine presets'),
			('Unity', 'Unity Engine', 'Unity engine presets')
        ],
		description="Standard presets for the selected game engine",
		name = "Game Engine Presets",
		default = 'UE4'
    )

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        col = box.column(align=True)
        row = col.row(align = True)
        row.label("Texel Density Units:")
        # TODO drop down for meters, centimeters
        col.prop(self, "game_engine", icon='RESTRICT_VIEW_OFF')
        if self.game_engine == 'UE4':
            col.label(text="Using Unreal Engine Presets: ")
        elif self.game_engine == 'Unity':
            col.label(text="Using Unity Engine Presets: ")

        # TODO quick export path

        box.separator()
        box = layout.box()
        box.label(text = "More Info and Other Junk: ")
        row = box.row(align=True)
        # TODO docs
        row.operator('wm.url_open', text='Donate', icon='HELP').url = 'https://gumroad.com/l/KFvsF'
        row.operator('wm.url_open', text='GitHub Code', icon='WORDWRAP_ON').url = 'https://github.com/bruceevans/betools-blender'
        row.operator('wm.url_open', text='My Stuff', icon='HELP').url = 'https://www.brucein3d.com'


## PIE MENUS


class BETOOLS_MT_PieMenu(Menu):
    """ Base class for betools' piemenus
    """

    bl_label = ""
    def __init__(self, name):
        bl_label = str(name)
        self.label = bl_label
        self.pie_menu = self.layout.menu_pie()

    def draw(self, context):
        pass


class BETOOLS_MT_VertexMenu(BETOOLS_MT_PieMenu):
    def __init__(self):
        BETOOLS_MT_PieMenu.__init__(self, "Vertex")

    def draw(self, context):

        self.pie_menu.operator("mesh.merge", text = "Merge Center", icon = "STICKY_UVS_VERT").type = 'CENTER' # TODO wrap
        self.pie_menu.operator("mesh.be_bevel", text = "Chamfer Vertices", icon_value = _icon.getIcon("CHAMFER"))
        self.pie_menu.operator("mesh.delete", text = "Delete Vertices", icon = "X").type = 'VERT'
        self.pie_menu.operator("mesh.merge", text = "Merge Last", icon = "TRACKING_FORWARDS_SINGLE").type = 'LAST' # TODO wrap
        self.pie_menu.operator("mesh.merge", text = "Merge First", icon = "TRACKING_BACKWARDS_SINGLE").type = 'FIRST' # TODO wrap
        self.pie_menu.operator("mesh.remove_doubles", text = "Merge Distance", icon = "AUTOMERGE_OFF")
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool", icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("mesh.vertices_smooth", text = "Smooth Vertices", icon = "SPHERECURVE")


class BETOOLS_MT_EdgeMenu(BETOOLS_MT_PieMenu):
    def __init__(self):
        BETOOLS_MT_PieMenu.__init__(self, "Edge")

    def draw(self, context):
        self.pie_menu.operator("mesh.loopcut_slide", text = "Loop Cut", icon = "VIEW_ORTHO")
        self.pie_menu.operator("transform.edge_crease", text = "Crease", icon = "LINCURVE")
        self.pie_menu.operator("mesh.dissolve_edges", text = "Dissolve Edges", icon = "X")
        self.pie_menu.operator("mesh.bridge_edge_loops", text = "Bridge", icon_value = _icon.getIcon("BRIDGE"))
        self.pie_menu.operator("mesh.be_bevel", text = "Bevel", icon = "MOD_BEVEL")
        self.pie_menu.operator("mesh.extrude_edges_move", text = "Extrude", icon_value = _icon.getIcon("EDGE_EXT"))
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool", icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("transform.edge_slide", text = "Edge Slide", icon = "MOD_SIMPLIFY")


class BETOOLS_MT_FaceMenu(BETOOLS_MT_PieMenu):
    def __init__(self):
        BETOOLS_MT_PieMenu.__init__(self, "Face")

    def draw(self, context):
        self.pie_menu.operator("mesh.extrude_region_shrink_fatten", text = "Extrude by Normals", icon = "NORMALS_FACE")
        self.pie_menu.operator("mesh.faces_shade_smooth", text = "Shade Smooth", icon = "SPHERECURVE")
        self.pie_menu.operator("mesh.delete", text = "Delete Faces", icon = "X").type = 'FACE'
        self.pie_menu.operator("mesh.smart_extract", text = "Smart Extract", icon = "PIVOT_CURSOR")
        self.pie_menu.operator("mesh.inset", text = "Inset Faces", icon = "OBJECT_DATA")
        self.pie_menu.operator("mesh.flip_normals", text = "Flip Normals", icon = "UV_SYNC_SELECT")
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool",  icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("mesh.faces_shade_flat", text = "Shade Flat", icon = "LINCURVE")


class BETOOLS_MT_MeshMenu(BETOOLS_MT_PieMenu):
    def __init__(self):
        BETOOLS_MT_PieMenu.__init__(self, "Mesh")

    def draw(self, context):
        self.pie_menu.operator("mesh.separate", text = "Split by Loose Parts", icon = "MOD_EXPLODE").type = 'LOOSE'
        self.pie_menu.operator("object.shade_flat", text = "Flat Shade", icon = "LINCURVE")
        self.pie_menu.operator("mesh.be_pivot2cursor", text = "Pivot to Cursor", icon = "EMPTY_ARROWS")

        freeze_transforms = self.pie_menu.operator("object.transform_apply", text = "Apply All Transforms", icon = "EMPTY_AXIS")
        freeze_transforms.location = True
        freeze_transforms.rotation = True
        freeze_transforms.scale = True

        self.pie_menu.operator("object.transforms_to_deltas", text = "Apply Delta Transforms", icon = "ORIENTATION_GLOBAL").mode = 'ALL'
        self.pie_menu.operator("object.shade_smooth", text = "Smooth Shade", icon = "SPHERECURVE")
        self.pie_menu.operator("wm.call_menu_pie", text = "Mirror Object", icon = "RIGHTARROW_THIN").name = "BETOOLS_MT_MirrorMenu"
        self.pie_menu.operator("mesh.be_center_pivot", text = "Center Pivot", icon = "OBJECT_ORIGIN")


class BETOOLS_MT_MirrorMenu(BETOOLS_MT_PieMenu):
    def __init__(self):
        BETOOLS_MT_PieMenu.__init__(self, "Mirror")

    def draw(self, context):
        self.pie_menu.operator("mesh.smart_mirror", text = "Mirror X", icon_value = _icon.getIcon("MIRROR_X")).direction = 'X'
        self.pie_menu.operator("mesh.smart_mirror", text = "Mirror Y", icon_value = _icon.getIcon("MIRROR_Y")).direction = 'Y'
        self.pie_menu.operator("wm.call_menu_pie", text = "Back", icon = "FILE_PARENT").name = "MeshMenu"
        self.pie_menu.operator("mesh.smart_mirror", text = "Mirror Z", icon_value = _icon.getIcon("MIRROR_Z")).direction = 'Z'


class BETOOLS_OT_PieCall(bpy.types.Operator):
    """ Main operator to call the pie menus
    """

    bl_idname = "view3d.b_modeling_hot_box"
    bl_label = "Be Tools - Modeling Hot Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.get_menu_context()
        return {'FINISHED'}

    def get_menu_context(self):
        context_mode = bpy.context.object.mode
        selectionMode = tuple(bpy.context.scene.tool_settings.mesh_select_mode)

        if context_mode == "OBJECT":
            bpy.ops.wm.call_menu_pie(name="BETOOLS_MT_MeshMenu")
            return
        try:
            bpy.ops.wm.call_menu_pie(name="BETOOLS_MT_{}Menu".format(_constants.SELECTION_MODES[selectionMode].capitalize()))
        except AttributeError:
            print("No objects currently in the scene")
            pass


## 3D VIEW MENUS


class UI_PT_BEToolsPanel(Panel):
    """ Main side panel in the 3D View
    """

    bl_label = "Be Tools"
    bl_category = "Be Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        layout.label(text="Viewport Display: ")
        box = layout.box()

        # row = layout.column().row(align=True)
        col = box.column(align=True)

        col.operator("mesh.be_toggle_wireframe", text = "Toggle Wireframe", icon = "SHADING_WIRE")
        col.operator("mesh.be_toggle_shaded", text = "Toggle Shaded", icon = "SHADING_SOLID")
        col.operator("view3d.toggle_xray", text = "Toggle XRay", icon = "XRAY")

        layout.label(text="Snapping: ")
        box = layout.box()

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("mesh.be_vert_snap", text = "Vertex", icon = "SNAP_VERTEX")
        row.operator("mesh.be_closest_vert_snap", text = "Close Vert", icon = "SNAP_GRID")
        row = col.row(align=True)
        row.operator("mesh.be_grid_snap", text = "Grid", icon = "SNAP_INCREMENT")

        object = context.active_object
        if object is None or len(bpy.context.selected_objects) == 0:
            layout.label(text='Select a Mesh!')
        else:
            layout.label(text="Pivot: ")
            box = layout.box()
            # row = layout.column().row(align=True)
            col = box.column(align=True)
            row=col.row(align=True)
            row.alert = True if _settings.edit_pivot_mode else False
            row.operator("mesh.be_editpivot", text = "Edit Pivot" if not _settings.edit_pivot_mode else "Set Pivot", icon = "OBJECT_ORIGIN")
            col.operator("mesh.be_center_pivot", text = "Center Pivot", icon = "OBJECT_ORIGIN")
            col.operator("mesh.be_pivot2cursor", text = "Pivot to Cursor", icon = "EMPTY_ARROWS")
            col.operator("view3d.snap_cursor_to_center", text = "Cursor to Origin")  # TODO ICON

            layout.label(text="Mesh Tools: ")

            box = layout.box()
            col = box.column(align=True)
            row = col.row(align=True)
            row.operator("mesh.smart_mirror", text = "X", icon_value = _icon.getIcon("MIRROR_X")).direction='X'
            row.operator("mesh.smart_mirror", text = "Y", icon_value = _icon.getIcon("MIRROR_Y")).direction='Y'
            row.operator("mesh.smart_mirror", text = "Z", icon_value = _icon.getIcon("MIRROR_Z")).direction='Z'

            row = col.row(align=True)
            row.operator("mesh.lattice_2", text = "2x2", icon_value = _icon.getIcon("LATTICE_2"))
            row.operator("mesh.lattice_3", text = "3x3", icon_value = _icon.getIcon("LATTICE_3"))
            row.operator("mesh.lattice_4", text = "4x4", icon_value = _icon.getIcon("LATTICE_4"))

            row = col.row(align=True)
            row.operator("mesh.smart_extract", text = "Smart Extract") # TODO Icon

            col = box.column(align=True)
            scene = context.scene
            row = col.row(align=True)
            row.prop_search(scene, "snap_object", bpy.data, "objects", text = "") # TODO icon

            row = col.row(align=True)
            row.operator("mesh.be_snap_to_face", text = "Snap Obj to Sel Face") # TODO icon

            mesh = bpy.context.object.data

            layout.label(text="Shading: ")
            box = layout.box()

            col = box.column(align=False)
            col.use_property_decorate = False

            if mesh:
                row = col.row(align=True)
                row.prop(mesh, "use_auto_smooth", text=" Auto Smooth")
                row.active = mesh.use_auto_smooth and not mesh.has_custom_normals

                row = col.row(align=True)
                row.prop(mesh, "auto_smooth_angle", text="")
                row.prop_decorator(mesh, "auto_smooth_angle")

            col = box.column(align=True)
            col.operator("object.shade_smooth", text = "Shade Smooth", icon = "SPHERECURVE")
            col.operator("object.shade_flat", text = "Shade Flat", icon = "LINCURVE")
            col.operator("mesh.be_recalc_normals", text = "Recalculate Normals", icon = "NORMALS_FACE")
            col.operator("mesh.be_toggle_fo", text = "Show Face Orientation", icon = "ORIENTATION_NORMAL")

            layout.label(text="UVs: ")
            box = layout.box()
            col = box.column(align=True)
            col.operator("mesh.seams_from_hard_edge", text = "Hard Edges To Seams", icon = "MOD_EDGESPLIT")
            col.operator("uv.unwrap", text = "Unwrap Faces", icon = "FACESEL")
            col.operator('uv.project_from_view', text = 'Cam Project', icon = 'CON_CAMERASOLVER')

            row = col.row(align=True)
            row.operator('uv.be_axis_project', text = "X Proj").axis='X'
            row.operator('uv.be_axis_project', text = "Y Proj").axis='Y'
            row.operator('uv.be_axis_project', text = "Z Proj").axis='Z'


class UI_PT_CollisionPanel(Panel):
    """ Main side panel in the 3D View
    """

    bl_label = "Collision Tools"
    bl_category = "Be Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # TODO Add ops based on prefs
        # TODO Context Sensitive
        layout = self.layout
        col = layout.column(align=True)
        object = context.active_object
        if object is None or len(bpy.context.selected_objects) == 0:
            col.label(text='Select a Mesh!')
        else:
            layout.label(text='UE4 Collision: ')
            box = layout.box()
            col = box.column()
            row = col.row(align=True)
            row.operator('mesh.be_ucx_hull', text = "UCX Convex")
            row.operator('mesh.be_ucx_box_collision', text = "UCX Box")
            row = col.row(align=True)
            row.operator('mesh.be_ubx_collision', text = "UBX")
            row.operator('mesh.be_usp', text = "USP")
            row.operator('mesh.be_ucp', text = "UCP")


class UI_PT_ExportPanel(Panel):
    """ Main side panel in the 3D View
    """

    bl_label = "I/O"
    bl_category = "Be Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        layout = self.layout
        layout.label(text="Export: ")
        box = layout.box()
        col = box.column(align=True)
        col.operator('mesh.be_export_selected_fbx', text = 'Export Sel as FBX')
        col.operator('mesh.be_export_scene_fbx', text = 'Export FBX')
        # TODO simple obj export to temp area


###############################################
# UV Panels
###############################################


import bmesh


class UI_PT_UVImage(Panel):
    bl_label = "BE Tools"
    bl_category = "Be Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):

        settings = context.scene.betools_settings

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)

        row = col.row(align = True)
        row.label(text="Map Size: ")
        row.prop(settings, "map_size_dropdown", text="")

        row = col.row(align = True)
        row.prop(settings, "checker_map_dropdown", text="")
        row.operator(
            'uv.be_assign_mat',
            text='Assign',
            icon="TEXTURE_DATA"
            ).size=int(settings.map_size_dropdown)

        row = col.row(align = True)
        row.operator(
            'uv.be_create_image',
            text='Create Blank Image',
            icon="MESH_PLANE"
            ).size=int(settings.map_size_dropdown)

        # TODO padding


class UI_PT_UVUtils(Panel):
    bl_category = "Be Tools"
    bl_label = "Utilities"
    bl_parent_id = "UI_PT_UVImage"
    bl_region_type = "UI"
    bl_space_type = "IMAGE_EDITOR"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        settings = context.scene.betools_settings
        layout = self.layout
        box = layout.box()

        col = box.column(align=True)
        row = col.row(align = True)
        row.label(text="UV Channels:")
        row = col.row(align = True)
        group = row.row(align=True)
        group.prop(settings, "uv_maps", text="")
        group = row.row(align=True)
        group.operator('uv.be_modify_uv_channel', text="", icon = 'GREASEPENCIL')
        group.operator('uv.be_add_uv_map', text="", icon = 'ADD')
        group.operator('uv.be_remove_uv_map', text="", icon = 'REMOVE')
        if _settings.uv_map_rename_mode:
            row = col.row(align = True)
            row.prop(settings, "uv_map_new_name", text="")
            row.operator('uv.be_uv_rename', text = "", icon='CHECKMARK')

        col = box.column(align=True)
        row = col.row()
        row.label(text="UV Stretch:")
        row.prop(settings, "show_uv_stretch", text="")
        row.prop(settings, "uv_stretch_type", text = "")

        col = box.column(align=True)
        row = col.row(align=True)
        row.operator("uv.export_layout", text="Export UV Layout", icon="RADIOBUT_ON")


class UI_PT_UVTransform(Panel):
    """ Main panel for the UV image editor
    """

    bl_label = "Transform"
    bl_category = "Be Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout
        box = layout.box()

        settings = context.scene.betools_settings

        col = box.column(align=True)
        row = col.row(align=True)
        row.prop(settings, "translate_u")
        row.prop(settings, "translate_v")
        row.operator('uv.be_translate', text='', icon="RADIOBUT_ON")

        row = col.row(align=True)
        row.prop(settings, "scale_u")
        row.prop(settings, "scale_v")
        row.operator('uv.be_scale', text='', icon="RADIOBUT_ON")

        row = col.row(align=True)
        row.prop(settings, "angle")
        row.operator('uv.be_rotate', text='', icon="RADIOBUT_ON").angle = settings.angle

    
class UI_PT_UVLayout(Panel):
    """ Main panel for the UV image editor
    """

    bl_label = "Layout"
    bl_category = "Be Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"

    def draw(self, context):
        settings = context.scene.betools_settings

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        
        row = col.row(align=True)
        row.operator('uv.be_flip', text="Flip H", icon="RADIOBUT_ON").direction = 'HORIZONTAL'
        row.operator('uv.be_flip', text="Flip V", icon="RADIOBUT_ON").direction = 'VERTICAL'
        row.separator()
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'LEFTTOP'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'CENTERTOP'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'RIGHTTOP'

        row = col.row(align=True)
        row.operator('uv.be_rotate', text='-90', icon="RADIOBUT_ON").angle=-90
        row.operator('uv.be_rotate', text='90', icon="RADIOBUT_ON").angle=90
        row.separator()
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'LEFTCENTER'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'CENTER'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'RIGHTCENTER'

        row = col.row(align=True)
        row.operator('uv.be_fit', text="Fit", icon="RADIOBUT_ON")
        row.operator('uv.be_fill', text='Fill', icon="RADIOBUT_ON")
        row.separator()
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'LEFTBOTTOM'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'CENTERBOTTOM'
        row.operator('uv.be_snap_island', text="", icon="RADIOBUT_ON").direction = 'RIGHTBOTTOM'

        col = box.column(align=True)
        col.operator('uv.be_orient_edge', text="Orient to Edge", icon="RADIOBUT_ON")
        col.operator("uv.be_stack", text='Stack Islands', icon="RADIOBUT_ON")
        col.operator("uv.be_uv_squares_by_shape", text="Rectify", icon="RADIOBUT_ON")
        col.operator("uv.be_uv_squares", text = "Squarify", icon="RADIOBUT_ON")
        col.operator("uv.be_uv_face_rip", text = "Rip Faces", icon="RADIOBUT_ON")

        row = col.row(align=True)
        row.operator("uv.pin", text="Pin UVs", icon="RADIOBUT_ON").clear=False
        row.operator("uv.pin", text="Unpin UVs", icon="RADIOBUT_ON").clear=True

        col = box.column(align=True)
        row = col.row(align=True)
        row.label(text = "Relax Strength: ")
        row.prop(settings, "relax_iterations", text="")
        row = col.row(align=True)
        row.operator("uv.minimize_stretch", text="Relax UV Angles").iterations=settings.relax_iterations * 100

        col = box.column(align=True)
        row = col.row(align=True)
        row.label(text="Padding: ")
        row.prop(settings, "sort_padding", text = "")
        row = col.row(align=True)
        row.operator("uv.be_island_sort", text="Sort H", icon="RADIOBUT_ON").axis = 'HORIZONTAL'
        row.operator("uv.be_island_sort", text="Sort V", icon="RADIOBUT_ON").axis = 'VERTICAL'

        row = col.row(align=True)
        row.operator("uv.pack_islands", text = "Pack Islands", icon="RADIOBUT_ON").margin = settings.pack_padding


class UI_PT_UVTexel(Panel):
    """ Main panel for modifying texel density
    """

    bl_label = "Texel"
    bl_category = "Be Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):

        uv_props = context.scene.betools_settings

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label(text="Texel Density: ")
        row.prop(uv_props, "texel_density", text = "")
        row = col.row(align=True)
        row.operator("uv.be_get_texel", text="Get", icon="RADIOBUT_ON")
        row.operator("uv.be_set_texel", text="Set", icon="RADIOBUT_ON")

        col = box.column(align=True)
        row = col.row()
        row.label(text="Texel Cubes: ", icon="MESH_CUBE")
        row = col.row(align=True)
        row.operator("uv.be_cube_helper", text=".5m").size = ".5M"
        row.operator("uv.be_cube_helper", text="1m").size = "1M"
        row.operator("uv.be_cube_helper", text="2m").size = "2M"
        row.operator("uv.be_cube_helper", text="4m").size = "4M"


class UI_PT_UVColorID(Panel):
    """ Create and modify ID maps
    """

    bl_label = "Color ID"
    bl_category = "Be Tools"
    bl_space_type = "IMAGE_EDITOR"
    bl_region_type = "UI"
    bl_options = {'DEFAULT_CLOSED'}

    def draw(self, context):
        # Image creation and generation
        settings = context.scene.betools_settings

        layout = self.layout
        box = layout.box()
        col = box.column(align=True)
        row = col.row(align=True)
        row.label(text="Material Name: ")
        row = col.row(align=True)
        row.prop(settings, "material_name", text = "")
        row.operator("uv.be_add_color", text="", icon="ADD")
        row.operator("uv.be_remove_color", text="", icon="REMOVE")

        col = box.column(align=True)

        for i in range(settings.color_id_count):
            row = col.row(align=True)
            row.label(text=getattr(settings, "color_id_{}_name".format(i)))
            row.prop(settings, "color_id_{}".format(i), text="")
            row.operator("uv.be_enable_rename_color", text="", icon="GREASEPENCIL").index=i
            row.operator("uv.be_assign_color", text="", icon="CHECKMARK").index=i
            if getattr(settings, "color_id_{}_rename".format(i)):
                row = col.row(align=True)
                row.prop(settings, "rename_material", text="")
                row.operator("uv.be_rename_color", text="", icon="CHECKMARK").index=i

        col = layout.column(align=True)
        row=col.row(align=True)
        row.label(text="Bleed: ")
        row.prop(settings, "color_id_pixel_bleed", text = "")

        col = layout.column(align=True)
        col.scale_y = 1.75
        bake = col.operator("uv.be_bake_id", text="Bake ID Map", icon="RADIOBUT_ON")
        bake.margin = settings.color_id_pixel_bleed
        bake.size = int(settings.map_size_dropdown)

        col = layout.column()
        col.operator("uv.be_clear_id_mats", text="Clear ID Materials")


bpy.types.Scene.snap_object = bpy.props.StringProperty()
