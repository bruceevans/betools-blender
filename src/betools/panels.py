#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import os
import bpy
import bpy.utils.previews
from bpy.types import Menu
from bpy.types import Panel
from . ops import *


class PieMenu(Menu):
    bl_label = ""
    def __init__(self, name):
        bl_label = str(name)
        self.label = bl_label
        self.pie_menu = self.layout.menu_pie()

    def draw(self, context):
        pass


class VertMenu(PieMenu):
    def __init__(self):
        PieMenu.__init__(self, "Vertex")

    def draw(self, context):

        self.pie_menu.operator("mesh.merge", text = "Merge Center", icon = "STICKY_UVS_VERT").type = 'CENTER'
        self.pie_menu.operator("mesh.be_bevel", text = "Chamfer Vertices", icon_value = get_icon("CHAMFER"))
        self.pie_menu.operator("mesh.delete", text = "Delete Vertices", icon = "X").type = 'VERT'
        self.pie_menu.operator("mesh.merge", text = "Merge Last", icon = "TRACKING_FORWARDS_SINGLE").type = 'LAST'
        self.pie_menu.operator("mesh.merge", text = "Merge First", icon = "TRACKING_BACKWARDS_SINGLE").type = 'FIRST'
        self.pie_menu.operator("mesh.remove_doubles", text = "Merge Distance", icon = "AUTOMERGE_OFF")
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool", icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("mesh.vertices_smooth", text = "Smooth Vertices", icon = "SPHERECURVE")


class EdgeMenu(PieMenu):
    def __init__(self):
        PieMenu.__init__(self, "Edge")

    def draw(self, context):
        self.pie_menu.operator("mesh.loopcut_slide", text = "Loop Cut", icon = "VIEW_ORTHO")
        self.pie_menu.operator("transform.edge_crease", text = "Crease", icon = "LINCURVE")
        self.pie_menu.operator("mesh.dissolve_edges", text = "Dissolve Edges", icon = "X")
        self.pie_menu.operator("mesh.bridge_edge_loops", text = "Bridge", icon_value = get_icon("BRIDGE"))
        self.pie_menu.operator("mesh.be_bevel", text = "Bevel", icon = "MOD_BEVEL")
        self.pie_menu.operator("mesh.extrude_edges_move", text = "Extrude", icon_value = get_icon("EDGE_EXT"))
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool", icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("transform.edge_slide", text = "Edge Slide", icon = "MOD_SIMPLIFY")


class FaceMenu(PieMenu):
    def __init__(self):
        PieMenu.__init__(self, "Face")

    def draw(self, context):
        self.pie_menu.operator("mesh.extrude_region_shrink_fatten", text = "Extrude by Normals", icon = "NORMALS_FACE")
        self.pie_menu.operator("mesh.faces_shade_smooth", text = "Shade Smooth", icon = "SPHERECURVE")
        self.pie_menu.operator("mesh.delete", text = "Delete Faces", icon = "X").type = 'FACE'
        self.pie_menu.operator("mesh.smart_extract", text = "Smart Extract", icon = "PIVOT_CURSOR")
        self.pie_menu.operator("mesh.inset", text = "Inset Faces", icon = "OBJECT_DATA")
        self.pie_menu.operator("mesh.flip_normals", text = "Flip Normals", icon = "UV_SYNC_SELECT")
        self.pie_menu.operator("mesh.knife_tool", text = "Knife Tool",  icon = "RESTRICT_SELECT_ON")
        self.pie_menu.operator("mesh.faces_shade_flat", text = "Shade Flat", icon = "LINCURVE")


class MeshMenu(PieMenu):
    def __init__(self):
        PieMenu.__init__(self, "Mesh")

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
        self.pie_menu.operator("wm.call_menu_pie", text = "Mirror Object", icon = "RIGHTARROW_THIN").name = "MirrorMenu"
        self.pie_menu.operator("mesh.be_center_pivot", text = "Center Pivot", icon = "OBJECT_ORIGIN")


class MirrorMenu(PieMenu):
    def __init__(self):
        PieMenu.__init__(self, "Mirror")

    def draw(self, context):
        self.pie_menu.operator("mesh.smart_mirror_x", text = "Mirror X", icon_value = get_icon("MIRROR_X"))
        self.pie_menu.operator("mesh.smart_mirror_y", text = "Mirror Y", icon_value = get_icon("MIRROR_Y"))
        self.pie_menu.operator("wm.call_menu_pie", text = "Back", icon = "FILE_PARENT").name = "MeshMenu"
        self.pie_menu.operator("mesh.smart_mirror_z", text = "Mirror Z", icon_value = get_icon("MIRROR_Z"))


class VIEW3D_OT_PIE_CALL(bpy.types.Operator):
    bl_idname = "view3d.b_modeling_hot_box"
    bl_label = "BE Tools - Modeling Hot Box"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        self.get_menu_context()
        return {'FINISHED'}

    def get_menu_context(self):
        try:
            context_mode = bpy.context.object.mode
            selection_mode = tuple(bpy.context.scene.tool_settings.mesh_select_mode)

            if context_mode == "OBJECT":
                bpy.ops.wm.call_menu_pie(name="MeshMenu")
                return
            else:
                if selection_modes[selection_mode] == "VERTEX":
                    bpy.ops.wm.call_menu_pie(name="VertMenu")
                elif selection_modes[selection_mode] == "EDGE":
                    bpy.ops.wm.call_menu_pie(name="EdgeMenu")
                else:
                    bpy.ops.wm.call_menu_pie(name="FaceMenu")
        except AttributeError:
            print("No objects currently in the scene")
            pass


class BEToolsPanel(Panel):

    bl_idname = "BE_Tools_Panel"
    bl_label = "BE Tools Panel"
    bl_category = "BE Tools"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"

    def draw(self, context):

        mesh_layout = self.layout
        mesh_layout.label(text="Mesh Tools")
        mesh_column = mesh_layout.column()
        mesh_column.operator("mesh.be_center_pivot", text = "Center Pivot", icon = "OBJECT_ORIGIN")
        mesh_column.operator("mesh.be_pivot2cursor", text = "Pivot to Cursor", icon = "EMPTY_ARROWS")
        mesh_column.operator("mesh.be_toggle_wireframe", text = "Toggle Wireframe", icon_value = get_icon("WIRE"))
        mesh_column.operator("mesh.lattice_2", text = "2x2 Lattice", icon_value = get_icon("LATTICE_2"))
        mesh_column.operator("mesh.lattice_3", text = "3x3 Lattice", icon_value = get_icon("LATTICE_3"))
        mesh_column.operator("mesh.lattice_4", text = "4x4 Lattice", icon_value = get_icon("LATTICE_4"))
        mesh_column.operator("mesh.smart_mirror_x", text = "Mirror X", icon_value = get_icon("MIRROR_X"))
        mesh_column.operator("mesh.smart_mirror_y", text = "Mirror Y", icon_value = get_icon("MIRROR_Y"))
        mesh_column.operator("mesh.smart_mirror_z", text = "Mirror Z", icon_value = get_icon("MIRROR_Z"))
        mesh_column.operator("mesh.be_recalc_normals", text = "Recalculate Normals", icon = "NORMALS_FACE")
        mesh_column.operator("mesh.be_toggle_fo", text = "Show Face Orientation", icon = "ORIENTATION_NORMAL")
        mesh_column.operator("mesh.be_auto_smooth_30", text = "Auto Smooth 30", icon_value = get_icon("AS_30"))
        mesh_column.operator("mesh.be_auto_smooth_45", text = "Auto Smooth 45", icon_value = get_icon("AS_45"))
        mesh_column.operator("mesh.be_auto_smooth_60", text = "Auto Smooth 60", icon_value = get_icon("AS_60"))
        mesh_column.operator("mesh.seams_from_hard_edge", text = "Hard Edges To Seams", icon = "MOD_EDGESPLIT")

        """
        face_layout = self.layout
        face_layout.label(text="Face Tools")
        face_column = face_layout.column()
        face_column.operator("mesh.extrude_region_shrink_fatten", text = "Extrude by Normals", icon = "NORMALS_FACE")
        face_column.operator("mesh.inset", text = "Inset Faces", icon = "OBJECT_DATA")
        face_column.operator("mesh.flip_normals", text = "Flip Normals", icon = "UV_SYNC_SELECT")
        face_column.operator("mesh.smart_extract", text = "Smart Extract", icon = "PIVOT_CURSOR")

        edge_layout = self.layout
        edge_layout.label(text="Edge Tools")
        edge_column = edge_layout.column()
        edge_column.operator("mesh.loopcut_slide", text = "Loop Cut", icon = "VIEW_ORTHO")
        edge_column.operator("mesh.be_bevel", text = "Edge Bevel", icon = "MOD_BEVEL")
        edge_column.operator("mesh.extrude_edges_move", text = "Extrude Edges", icon_value = get_icon("EDGE_EXT"))
        edge_column.operator("transform.edge_crease", text = "Crease", icon = "LINCURVE")
        edge_column.operator("mesh.bridge_edge_loops", text = "Bridge", icon_value = get_icon("BRIDGE"))

        vert_layout = self.layout
        vert_layout.label(text="Vertex Tools")
        vert_column = vert_layout.column()
        vert_column.operator("mesh.be_bevel", text = "Chamfer", icon_value = get_icon("CHAMFER"))
        vert_column.operator("mesh.remove_doubles", text = "Merge Distance", icon = "AUTOMERGE_OFF")
        vert_column.operator("mesh.merge", text = "Merge Center", icon = "STICKY_UVS_VERT").type = 'CENTER'

        try:
            vert_column.operator("mesh.merge", text = "Merge Last", icon_value = get_icon("MERGE_LAST")).type = 'LAST'
        except TypeError:
            pass
        try:
            vert_column.operator("mesh.merge", text = "Merge First", icon_value = get_icon("MERGE_FIRST")).type = 'FIRST'
        except TypeError:
            pass
        """

        # TODO UV

        ue4_collision_layout = self.layout
        ue4_collision_layout.label(text="UE4 Collision Mesh")
        ue4_column = ue4_collision_layout.column()
        ue4_column.operator('mesh.be_ucx_hull', text = "UCX Convex Collision")
        ue4_column.operator('mesh.be_ucx_box_collision', text = "UCX Box Collision")
        ue4_column.operator('mesh.be_ubx_collision', text = "UBX Collision")
        ue4_column.operator('mesh.be_usp', text = "USP Collision")
        ue4_column.operator('mesh.be_ucp', text = "UCP Collision")

        export_layout = self.layout
        export_layout.label(text="Export")
        export_column = export_layout.column()
        export_column.operator('mesh.be_export_selected_fbx', text = 'Export Sel as FBX')
        export_column.operator('mesh.be_export_scene_fbx', text = 'Export FBX')


## ICONS ##

preview_collections = {}
preview_icons = bpy.utils.previews.new()

def get_icon(icon):
    return preview_icons[icon].icon_id

def register_icon(icon_file):
    icon_name = icon_file.split('.')[0]
    dir = os.path.join(os.path.dirname(__file__), "icons")
    preview_icons.load(icon_name, os.path.join(dir, icon_file), 'IMAGE')
