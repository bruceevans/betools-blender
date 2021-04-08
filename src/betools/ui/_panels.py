#################################################################
# Be Tools by Bruce Evans                                       #
# brucein3d@gmail.com                                           #
#################################################################

import os

import bpy

import bpy.utils.previews
from bpy.types import Menu
from bpy.types import Panel

from .. ops import *
from .. utils import _icon
from .. utils import _constants


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
        col.prop(self, "game_engine", icon='RESTRICT_VIEW_OFF')
        if self.game_engine == 'UE4':
            col.label(text="Using Unreal Engine Presets")
        elif self.game_engine == 'Unity':
            col.label(text="Using Unity Engine Presets")

        # TODO quick export path

        box.separator()
        box = layout.box()
        box.label(text = "More Info and Other Junk")
        row = box.row(align=True)
        # TODO docs
        row.operator('wm.url_open', text='Donate', icon='HELP').url = 'https://gumroad.com/l/KFvsF'
        row.operator('wm.url_open', text='GitHub Code', icon='WORDWRAP_ON').url = 'https://github.com/bruceevans/betools-blender'
        row.operator('wm.url_open', text='My Stuff', icon='HELP').url = 'https://www.brucein3d.com'


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

        # TODO wrap
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
        self.pie_menu.operator("mesh.smart_mirror_x", text = "Mirror X", icon_value = _icon.getIcon("MIRROR_X"))
        self.pie_menu.operator("mesh.smart_mirror_y", text = "Mirror Y", icon_value = _icon.getIcon("MIRROR_Y"))
        self.pie_menu.operator("wm.call_menu_pie", text = "Back", icon = "FILE_PARENT").name = "MeshMenu"
        self.pie_menu.operator("mesh.smart_mirror_z", text = "Mirror Z", icon_value = _icon.getIcon("MIRROR_Z"))


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


class UI_PT_BEToolsPanel(Panel):
    """ Main side panel in the 3D View
    """

    bl_label = "Be Tools Panel"
    bl_category = "Be Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        layout = self.layout

        layout.label(text="Viewport Display Modes")

        row = layout.column().row(align=True)

        row.operator("mesh.be_toggle_wireframe", text = "Wire", icon = "CUBE")
        row.operator("mesh.be_toggle_shaded", text = "Shade", icon = "MESH_CUBE")
        row.operator("view3d.toggle_xray", text = "XRay", icon = "XRAY")

        layout.label(text="Pivot")

        row = layout.column().row(align=True)
        row.operator("mesh.be_center_pivot", text = "Edit", icon = "OBJECT_ORIGIN")
        row.operator("mesh.be_center_pivot", text = "Center", icon = "OBJECT_ORIGIN")
        row.operator("mesh.be_pivot2cursor", text = "Cursor", icon = "EMPTY_ARROWS")

        layout.label(text="Mirror")

        row = layout.column().row(align=True)
        row.operator("mesh.smart_mirror_x", text = "X", icon_value = _icon.getIcon("MIRROR_X"))
        row.operator("mesh.smart_mirror_y", text = "Y", icon_value = _icon.getIcon("MIRROR_Y"))
        row.operator("mesh.smart_mirror_z", text = "Z", icon_value = _icon.getIcon("MIRROR_Z"))

        layout.label(text="Quick Lattice")

        row = layout.column().row(align=True)

        row.operator("mesh.lattice_2", text = "2x2", icon_value = _icon.getIcon("LATTICE_2"))
        row.operator("mesh.lattice_3", text = "3x3", icon_value = _icon.getIcon("LATTICE_3"))
        row.operator("mesh.lattice_4", text = "4x4", icon_value = _icon.getIcon("LATTICE_4"))

        layout.label(text="Auto Smooth")

        row = layout.column().row(align=True)

        row.operator("mesh.be_auto_smooth_30", text = "30", icon_value = _icon.getIcon("AS_30"))
        row.operator("mesh.be_auto_smooth_45", text = "45", icon_value = _icon.getIcon("AS_45"))
        row.operator("mesh.be_auto_smooth_60", text = "60", icon_value = _icon.getIcon("AS_60"))

        layout.label(text="Normals")

        row = layout.column().row(align=True)

        row.operator("mesh.be_recalc_normals", text = "Recalc", icon = "NORMALS_FACE")
        row.operator("mesh.be_toggle_fo", text = "Show", icon = "ORIENTATION_NORMAL")

        layout.label(text="Mesh Tools")

        row = layout.column().row(align=True)
        # TODO other tools?

        row.operator("mesh.smart_extract", text = "Smart Extract") # TODO Icon

        layout.label(text="UVs")

        col = layout.column(align=True)

        col.operator("mesh.seams_from_hard_edge", text = "Hard Edges To Seams", icon = "MOD_EDGESPLIT")

        # TODO Unwrap
        # Options for unwrap method and margin
        
        # TODO Projections (project from view in blender)

        # TODO Switch collision ops based on prefs
        layout.label(text='Collision Generation')

        col = layout.column(align=True)
        row = col.row(align=True)

        row.operator('mesh.be_ucx_hull', text = "UCX Convex")
        row.operator('mesh.be_ucx_box_collision', text = "UCX Box")
        col.operator('mesh.be_ubx_collision', text = "UBX")
        col.operator('mesh.be_usp', text = "USP")
        col.operator('mesh.be_ucp', text = "UCP")

        layout.label(text="Export")
        col = layout.column(align=True)
        col.operator('mesh.be_export_selected_fbx', text = 'Export Sel as FBX')
        col.operator('mesh.be_export_scene_fbx', text = 'Export FBX')
        # TODO simple obj export to temp area
