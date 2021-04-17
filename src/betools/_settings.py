# TODO choose game engine (ue4, unity, hide)

import bpy
import bmesh
import operator

uv_selection_mode = ''
uv_loops_selection = []
uv_pivot_selection = ''
uv_pivot_selection_position = (0, 0)

selection_mode = (False, False, True)
vert_selection = []     # indices
face_selection = []      # indices

game_engine = ''        # Unreal or Unity
