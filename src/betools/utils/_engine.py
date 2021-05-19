

UNREAL = {
    # Unit setup for Blender
    "SYSTEM_UNITS": {
        "UNIT_SYSTEM": "Metric",
        "UNIT_SCALE": 0.010000,
        "LENGTH": "Centimeters"
    },

    "BAKING" : {
        "GREEN_CHANNEL": "-Y"
    },

    # Mesh and rig fbx export settings
    "MESH_EXPORT": {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,               # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,          # apply transform
        "object_types": {'ARMATURE', 'MESH'},   # Tweaked
        "use_mesh_modifiers": True,             # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'EDGE',             # Tweaked
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": True,                     # Tweaked
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'-Z',             # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'ROOT',            # Tweaked
        "bake_anim": False,                     # don't need these for mesh exports
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": False,     # Tweaked
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Y',                    # Tweaked
        "axis_up": 'Z'                           # Tweaked
    },

    # Animation export settings
    "ANIM_EXPORT" : {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,               # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,          # apply transform
        "object_types": {'ARMATURE', 'MESH'},   # Tweaked
        "use_mesh_modifiers": True,             # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'EDGE',             # Tweaked
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": True,                     # Tweaked
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'-Z',             # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'ROOT',            # Tweaked
        "bake_anim": True,
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": False,     # Tweaked
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Y',                    # Tweaked
        "axis_up": 'Z'                           # Tweaked
    },

    "COLLISION_SETTINGS": {
        # Convex
        # Convex Cube
        # Sphere
        # Cylinder
        # Cube
    }
}

UNITY = {

    "SYSTEM_UNITS": {
    "UNIT_SYSTEM": "Metric",
    "UNIT_SCALE": 1.0000,
    "LENGTH": "Meters"
    },

    "BAKING" : {
        "GREEN_CHANNEL": "Y"
    },

    "MESH_EXPORT": {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,                # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,           # apply transform
        "object_types": {'ARMATURE', 'MESH'},    # Tweaked
        "use_mesh_modifiers": True,              # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'OFF',
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": False,
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'Y',              # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'NULL',            # Tweaked
        "bake_anim": False,                     # don't need these for mesh exports
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": True,     # Tweaked might need to test this TODO
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Z',                    # Tweaked
        "axis_up": 'Y'                           # Tweaked
    },

    "ANIM_EXPORT" : {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,                # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,           # apply transform
        "object_types": {'ARMATURE', 'MESH'},    # Tweaked
        "use_mesh_modifiers": True,              # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'OFF',
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": False,
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'Y',              # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'NULL',            # Tweaked
        "bake_anim": True,
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": True,     # Tweaked might need to test this TODO
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Z',                    # Tweaked
        "axis_up": 'Y'                           # Tweaked
    },
    "COLLISION_SETTINGS": {

    }
}

SOURCE = {

    "SYSTEM_UNITS": {
    "UNIT_SYSTEM": "Imperial",
    "UNIT_SCALE": 1.0000,
    "LENGTH": "Feet"
    },

    "MESH_EXPORT": {

    },

    "ANIM_EXPORT" : {

    },

    "COLLISION_SETTINGS": {

    }
}

GODOT = {
    "SYSTEM_UNITS": {
    "UNIT_SYSTEM": "Metric",
    "UNIT_SCALE": 1.0000,
    "LENGTH": "Meters"
    },
    
    "MESH_EXPORT": {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,                # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,           # apply transform
        "object_types": {'ARMATURE', 'MESH'},    # Tweaked
        "use_mesh_modifiers": True,              # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'OFF',
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": False,
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'Y',              # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'NULL',            # Tweaked
        "bake_anim": False,                     # don't need these for mesh exports
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": True,     # Tweaked might need to test this TODO
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Z',                    # Tweaked
        "axis_up": 'Y'                           # Tweaked
    },

    "ANIM_EXPORT" : {
        "filepath": '',
        "check_existing": True,
        "filter_glob":' *.fbx',
        "use_selection": True,                  # Tweaked
        "use_active_collection": False,
        "global_scale": 1.0,
        "apply_unit_scale": True,                # True for UE4
        "apply_scale_options": 'FBX_SCALE_NONE',
        # "use_space_transform": True,
        "bake_space_transform": False,           # apply transform
        "object_types": {'ARMATURE', 'MESH'},    # Tweaked
        "use_mesh_modifiers": True,              # True
        "use_mesh_modifiers_render": True,
        "mesh_smooth_type": 'OFF',
        "use_subsurf": False,
        "use_mesh_edges": False,
        "use_tspace": False,
        "use_custom_props": True,               # Tweaked
        "add_leaf_bones": False,
        "primary_bone_axis":'X',                # Tweaked
        "secondary_bone_axis":'Y',              # Tweaked
        "use_armature_deform_only": True,       # Tweaked
        "armature_nodetype": 'NULL',            # Tweaked
        "bake_anim": True,
        "bake_anim_use_all_bones": True,
        "bake_anim_use_nla_strips": True,
        "bake_anim_use_all_actions": True,     # Tweaked might need to test this TODO
        "bake_anim_force_startend_keying": True,
        "bake_anim_step": 1.0,
        "bake_anim_simplify_factor": 1.0,
        "path_mode": 'AUTO',
        "embed_textures": False,
        "batch_mode": 'OFF',
        "use_batch_own_dir": True,
        "use_metadata": True,
        "axis_forward": '-Z',                    # Tweaked
        "axis_up": 'Y'                           # Tweaked
    },
    
    "COLLISION_SETTINGS": {

    }
}

