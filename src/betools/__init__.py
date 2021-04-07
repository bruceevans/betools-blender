# ------------------------------------------------------------------------------
# BE Tools by Bruce Evans - brucein3d@gmail.com
# Thank you so much for supporting my work!  Please reach out with feedback,
# and other requests.  I would love to hear them.
# ------------------------------------------------------------------------------

bl_info = {
    "name": "BE Tools",
    "author": "Bruce Evans",
    "version": (1, 1, 0),
    "description": "Context sensitive pie menus for various modeling tasks, mimics Maya's shift + RMB functionality and a shelf like menu for easy access modeling functions",
    "blender": (2, 90, 0),
    "category": "User Interface"
}

if "bpy" in locals():
    import imp

    imp.reload(settings)
    imp.reload(panels)

    imp.reload(utils._constants)
    imp.reload(utils._uvs)

    imp.reload(ops._autosmooth)
    imp.reload(ops._bevel)
    imp.reload(ops._collision)
    imp.reload(ops._edge)
    imp.reload(ops._export)
    imp.reload(ops._hardedgeseam)
    imp.reload(ops._lattice)
    imp.reload(ops._mesh)
    imp.reload(ops._mirror)
    imp.reload(ops._pivot)
    imp.reload(ops._smartextract)
    imp.reload(ops._uv)
    imp.reload(ops._vert)
    imp.reload(ops._viewops)

else:
    import panels
    import settings

    from .ops import _autosmooth
    from .ops import _bevel
    from .ops import _collision
    from .ops import _edge
    from .ops import _export
    from .ops import _hardedgeseam
    from .ops import _lattice
    from .ops import _mesh
    from .ops import _mirror
    from .ops import _pivot
    from .ops import _smartextract
    from .ops import _uv
    from .ops import _vert
    from .ops import _viewops


import bpy
import os
import math
import string
import bpy.utils.previews

from bpy.types import Menu, Operator, Panel, UIList

from bpy.props import (
	StringProperty,
	BoolProperty,
	IntProperty,
	FloatProperty,
	FloatVectorProperty,
	EnumProperty,
	PointerProperty,
)


class PreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = __package__  # TODO what is this?

    game_engine : bpy.props.EnumProperty(
        items = [
            'Unreal Engine',
            'Unity'
        ],
        description = 'Preferred game engine',
        name = 'Game Engine',
        default = 'Unreal Engine'
    )

    # help/docs
    # github link
    # portfolio link

    def draw(self, context):
        layout = self.layout

        box = layout.box()
        col = box.column(align=True)
        col.prop(self, "game_engine", icon='RESTRICT_VIEW_OFF')
        if self.game_engine == 'Unreal Engine':
            col.label(text="Unreal Engine presets")
        elif self.game_engine == 'Unity':
            col.label(text="Unity engine presets")

        box.separator()
        box = layout.box()
        box.label(text = "More Info")
        col = box.column(align=True)
        col.operator('wm.url_open', text='Donate', icon='HELP').url = 'https://gumroad.com/l/KFvsF'
        

# SETTINGS?

addon_keymaps = []

classes = (
    BEToolsPanel,
    PieMenu,
    VertMenu,
    EdgeMenu,
    FaceMenu,
    MeshMenu,
    MirrorMenu,
    SmartExtract,
    SmartMirror,
    SmartMirrorX,
    SmartMirrorY,
    SmartMirrorZ,
    VIEW3D_OT_PIE_CALL,
    BEAutoSmooth,
    BEAutoSmooth30,
    BEAutoSmooth45,
    BEAutoSmooth60,
    SeamHardEdge,
    DivideLattice,
    Lattice,
    Lattice_2,
    Lattice_3,
    Lattice_4,
    CenterPivot,
    Pivot2Cursor,
    SmartBevel,
    ToggleWireFrame,
    UE4CollisionGenerator,
    UBXCollisionGenerator,
    UCXBoxCollisionGenerator,
    UCXHullCollisionGenerator,
    USPCollisionGenerator,
    UCPCollisionGenerator,
    ExportSelection,
    ExportScene,
    ToggleFaceOrientation,
    RecalcNormals
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

    # keymapping
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new(VIEW3D_OT_PIE_CALL.bl_idname, 'SPACE', 'PRESS')
    kmi.active = True
    addon_keymaps.append((km, kmi))

    ## ICONS ##

    icons = [
        "AS_30.png",
        "AS_45.png",
        "AS_60.png",
        "BRIDGE.png",
        "CHAMFER.png",
        "EDGE_EXT.png",
        "LATTICE_2.png",
        "LATTICE_3.png",
        "LATTICE_4.png",
        "MERGE_FIRST.png",
        "MERGE_LAST.png",
        "MIRROR_X.png",
        "MIRROR_Y.png",
        "MIRROR_Z.png",
        "VERT_SLIDE.png",
        "WIRE.png",
        "WIRE_SHADED.png"
    ]

    for icon in icons:
        panels.register_icon(icon)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
