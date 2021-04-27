#################################################################
# Be Tools by Bruce Evans                                       #
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
    imp.reload(ui._panels)
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
    imp.reload(ops._uv_rect)
    imp.reload(ops._vert)
    imp.reload(ops._viewops)
    imp.reload(ops._snapping)

else:
    from . import _settings
    from .ui import _panels

    from .utils import _constants
    from .utils import _uvs

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
    from .ops import _uv_rect
    from .ops import _vert
    from .ops import _viewops
    from .ops import _snapping


import bpy
        

classes = (
    _panels.BEPreferencesPanel,
    _panels.BETOOLS_MT_PieMenu,
    _panels.BETOOLS_MT_VertexMenu,
    _panels.BETOOLS_MT_EdgeMenu,
    _panels.BETOOLS_MT_FaceMenu,
    _panels.BETOOLS_MT_MeshMenu,
    _panels.BETOOLS_MT_MirrorMenu,
    _panels.BETOOLS_OT_PieCall,
    _panels.UI_PT_BEToolsPanel,
    _panels.UI_PT_CollisionPanel,
    _panels.UI_PT_ExportPanel,
    _panels.UI_PT_UVImage,
    _panels.UI_PT_UVTransform,
    _panels.UI_PT_UVLayout,
    _panels.UI_PT_UVTexel,
    _panels.UI_PT_UVColorID
)

addon_keymaps =[]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    # handle keymaps
    kc = bpy.context.window_manager.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D')
    kmi = km.keymap_items.new(_panels.BETOOLS_OT_PieCall.bl_idname, 'SPACE', 'PRESS', shift=True)
    kmi.active = True
    addon_keymaps.append((km, kmi))

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
