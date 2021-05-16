
import os
import bpy

_ICONS = [
    "be_accept.png",
    "be_add_image.png",
    "be_align.png",
    "be_bug.png",
    "be_cam.png",
    "be_checker.png",
    "be_edit.png",
    "be_export.png",
    "be_extract.png",
    "be_fill.png",
    "be_fit.png",
    "be_flip_hor.png",
    "be_flip_vert.png",
    "be_grid.png",
    "be_image.png",
    "be_lattice.png",
    "be_material.png",
    "be_move.png",
    "be_not_visible.png",
    "be_pack.png",
    "be_rectify.png",
    "be_rename.png",
    "be_pin.png",
    "be_rip.png",
    "be_rotate.png",
    "be_rotate_90.png",
    "be_rotate_neg_90.png",
    "be_scale.png",
    "be_shade_flat.png",
    "be_shade_smooth.png",
    "be_snap_bl.png",
    "be_snap_bm.png",
    "be_snap_br.png",
    "be_snap_ml.png",
    "be_snap_mm.png",
    "be_snap_mr.png",
    "be_snap_tl.png",
    "be_snap_tm.png",
    "be_snap_tr.png",
    "be_sort_hor.png",
    "be_sort_vert.png",
    "be_stack.png",
    "be_texture.png",
    "be_trash.png",
    "be_unpin.png",
    "be_visible.png",
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

previewCollections = {}
previewIcons = bpy.utils.previews.new()

def register_icon(iconFile):
    icon_name = os.path.splitext(iconFile)[0]
    directory = os.path.join(os.path.dirname(__file__), "icons")
    print(directory)
    previewIcons.load(icon_name, os.path.join(directory, iconFile), 'IMAGE')

for icon in _ICONS:
    register_icon(icon)

def get_icon(icon):
    return previewIcons[icon].icon_id
