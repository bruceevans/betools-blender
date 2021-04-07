
import os
import bpy

_ICONS = [
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

for icon in _ICONS:
    registerIcon(icon)

preview_collections = {}
preview_icons = bpy.utils.previews.new()

def getIcon(icon):
    return preview_icons[icon].icon_id

def registerIcon(iconFile):
    iconName = os.path.splitext(iconFile)[0]
    dir = os.path.join(os.path.dirname(__file__), "icons")
    preview_icons.load(iconName, os.path.join(dir, iconFile), 'IMAGE')