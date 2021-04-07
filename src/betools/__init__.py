#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

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

    imp.reload(_settings)
    # imp.reload(_panels)

    imp.reload(utils._constants)
    imp.reload(utils._uvs)

    """
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
    """
    imp.reload(ops._viewops)

else:
    from . import _settings
    # from . import _panels

    from .utils import _constants
    from .utils import _uvs

    """
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
    """
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


class BEPreferencesPanel(bpy.types.AddonPreferences):
    bl_idname = __package__  # TODO what is this?

    game_engine : bpy.props.EnumProperty(
        items = [
            ('UE4', 'Unreal Engine', 'Presets for the Unreal Engine'),  # TODO icon
            ('Unity', 'Unity', 'Presets for the Unity Engine')  # TODO icon
        ],
        description = 'Game engine presets',
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
        col.operator('wm.url_open', text='GitHub Code', icon='WORDWRAP_ON').url = 'https://github.com/bruceevans/betools-blender'
        

classes = (
    BEPreferencesPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()

"""
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
"""