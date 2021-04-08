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
    imp.reload(ops._vert)
    imp.reload(ops._viewops)

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
    from .ops import _vert
    from .ops import _viewops


import bpy
        

classes = (
    _panels.BEPreferencesPanel,
    _panels.PieMenu,
    _panels.VertMenu,
    _panels.EdgeMenu,
    _panels.FaceMenu,
    _panels.MeshMenu,
    _panels.MirrorMenu,
    _panels.VIEW3D_OT_PIE_CALL,
    _panels.BEToolsPanel,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

if __name__ == "__main__":
    register()
