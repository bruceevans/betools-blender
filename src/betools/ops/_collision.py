#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from mathutils import Vector


class UE4CollisionGenerator(bpy.types.Operator):
    # Parent class for collision mesh generation
    bl_idname = "mesh.be_ue4_collision_gen"
    bl_label = "UE4 Collision Generator"
    bl_description = "Create collision geometry for Unreal Engine 4"
    bl_options = {'REGISTER', 'UNDO'}

    def get_bounding_box(self):

        selection = bpy.context.active_object

        if selection.mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')

        vertices = selection.data.vertices
        vert_positions = [vertex.co @ selection.matrix_world for vertex in vertices]
        self.rotation = bpy.data.objects[selection.name].rotation_euler
        self.obj_location = bpy.data.objects[selection.name].location

        bb_min = Vector()
        bb_max = Vector()

        for axis in range(3):
            pos_list = [pos[axis] for pos in vert_positions]
            bb_max[axis] = max(pos_list)
            bb_min[axis] = min(pos_list)

        self.center = (bb_min + bb_max) / 2.0
        self.location = self.obj_location + self.center
        bounding_box = [bb_min, bb_max]

        return bounding_box

    def generate_bounding_box_verts(self, verts):  # bounding box min and max vector

        vertices = []
        vertex = [0, 0, 0]
        
        vertex = [verts[1].x, verts[1].y, verts[0].z]
        vertices.append(vertex) # min
        vertex = [verts[1].x, verts[0].y, verts[0].z]
        vertices.append(vertex)
        vertex = [verts[0].x, verts[0].y, verts[0].z]
        vertices.append(vertex)
        vertex = [verts[0].x, verts[1].y, verts[0].z]
        vertices.append(vertex)
        
        vertex = [verts[1].x, verts[1].y, verts[1].z]
        vertices.append(vertex)
        vertex = [verts[1].x, verts[0].y, verts[1].z]
        vertices.append(vertex)
        vertex = [verts[0].x, verts[0].y, verts[1].z]
        vertices.append(vertex)
        vertex = [verts[0].x, verts[1].y, verts[1].z]
        vertices.append(vertex)
    
        return vertices

    def generate_bounding_box_faces(self):
    
        faces = [
            (0, 1, 2, 3),
            (4, 7, 6, 5), 
            (0, 4, 5, 1),
            (1, 5, 6, 2),
            (2, 6, 7, 3),
            (4, 0, 3, 7)
            ]
        
        return faces

    def get_name(self, selection, coll_type):  # coll_type = "UBX_", "UCX_", etc.
        name = coll_type + selection.name
        collection = bpy.context.collection
        obj_counter = 0
        for obj in collection.objects:
            if name in obj.name:
                obj_counter += 1
        if obj_counter == 0:
            name = name + "_00"
        elif obj_counter < 10:
            name = name + "_0" + str(obj_counter)
        else:
            name = name + "_" + str(obj_counter)
        return name

    def apply_material(self, obj):

        if len(obj.material_slots) > 0:
            for mat in obj.material_slots:
                bpy.ops.object.material_slot_remove({'object': obj})

        # check if collision material exists
        mat_name = 'mat_collision'
        if self.material_exists(mat_name):
            # apply it
            mat = bpy.data.materials[mat_name]
            obj.data.materials.append(mat)
            bpy.context.object.active_material.blend_method = 'BLEND'
        else:
            mat = bpy.data.materials.new(name = mat_name)
            mat.use_nodes = True
            mat_shader = mat.node_tree.nodes["Principled BSDF"]
            mat_shader.inputs[0].default_value = (0, 1, 1, 1) # cyan color
            mat_shader.inputs[4].default_value = 0 # metallic
            mat_shader.inputs[5].default_value = 0 # specular
            mat_shader.inputs[7].default_value = 1 # roughness
            mat_shader.inputs[10].default_value = 0 # sheen
            mat_shader.inputs[12].default_value = 0 # clearcoat
            mat_shader.inputs[18].default_value = 0.1 # alpha
            obj.data.materials.append(mat)
            bpy.context.object.active_material.blend_method = 'BLEND'
        
    def material_exists(self, material_name):
        for mat in bpy.data.materials:
            if mat.name == material_name:
                return True
        return False

    @classmethod
    def poll(cls, context):
        if context.object is not None and bpy.context.active_object.mode == "OBJECT":
            return True


class UBXCollisionGenerator(UE4CollisionGenerator):
    bl_idname = "mesh.be_ubx_collision"
    bl_label = "UBX Collision Generator"
    bl_description = "Create UBX (Box) collision geometry for Unreal Engine 4"
    bl_options = {'REGISTER', 'UNDO'}

    def fill_bounding_box_mesh(self, name):
        
        collection = bpy.context.collection

        mesh = bpy.data.meshes.new("ubx_collision_mesh")
        bbox = self.get_bounding_box()
        verts = self.generate_bounding_box_verts(bbox)
        faces = self.generate_bounding_box_faces()
        mesh.from_pydata(verts, [], faces)

        obj = bpy.data.objects.new(name, mesh)
        obj.location = self.location - self.center

        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        self.apply_material(obj)

    def execute(self, context):
        selection = bpy.context.active_object
        self.fill_bounding_box_mesh(self.get_name(selection, "UBX_"))
        return {'FINISHED'}


class UCXBoxCollisionGenerator(UE4CollisionGenerator):
    bl_idname = "mesh.be_ucx_box_collision"
    bl_label = "UBX Collision Generator"
    bl_description = "Create UCX (Convex) collision geometry based on the objects bounding box for Unreal Engine 4"
    bl_options = {'REGISTER', 'UNDO'}

    def fill_bounding_box_mesh(self, name):
        
        collection = bpy.context.collection

        mesh = bpy.data.meshes.new("ucx_box_collision_mesh")
        bbox = self.get_bounding_box()
        verts = self.generate_bounding_box_verts(bbox)
        faces = self.generate_bounding_box_faces()
        mesh.from_pydata(verts, [], faces)

        obj = bpy.data.objects.new(name, mesh)
        obj.location = self.location - self.center

        collection.objects.link(obj)
        bpy.context.view_layer.objects.active = obj

        self.apply_material(obj)

    def execute(self, context):
        selection = bpy.context.active_object
        self.fill_bounding_box_mesh(self.get_name(selection, "UCX_"))
        return {'FINISHED'}


class UCXHullCollisionGenerator(UE4CollisionGenerator):
    bl_idname = "mesh.be_ucx_hull"
    bl_label = "UCX Hull Collision"
    bl_description = "Create convex collision for UE4"
    bl_options = {"REGISTER", "UNDO"}

    def duplicate_mesh(self):
        selection = bpy.context.active_object
        name = self.get_name(selection, "UCX_")
        bpy.ops.object.duplicate()

        selection = bpy.context.active_object

        # apply material
        self.apply_material(selection)

        self.apply_material(selection)
        selection.name = name

    def convex_hull(self):
        # set to edit mode
        bpy.ops.object.mode_set(mode = 'EDIT')
        bpy.ops.mesh.select_all(action='SELECT')
        # create hull
        bpy.ops.mesh.convex_hull()
        bpy.ops.object.mode_set(mode = 'OBJECT')

    def decimate(self):
        bpy.ops.object.modifier_add(type='DECIMATE')

    def execute(self, context):
        self.duplicate_mesh()
        self.convex_hull()
        self.decimate()
        return{'FINISHED'}

class USPCollisionGenerator(UE4CollisionGenerator):
    bl_idname = "mesh.be_usp"
    bl_label = "USP Collision"
    bl_description = "Create sphere collision for UE4"
    bl_options = {"REGISTER", "UNDO"}

    def get_radius(self):
        bbox = self.get_bounding_box()  # generates min and max
        dimensions = []
        x_dim = abs(bbox[1].x - bbox[0].x)
        dimensions.append(x_dim)
        y_dim = abs(bbox[1].y - bbox[0].y)
        dimensions.append(y_dim)
        z_dim = abs(bbox[1].z - bbox[0].z)
        dimensions.append(z_dim)
        sorted_dimensions = sorted(dimensions)
        a = sorted_dimensions[-1] / 2.0
        b = sorted_dimensions[-2] / 2.0
        r = math.sqrt(a*a+b*b)
        return r

    def make_sphere(self, rad, loc, rot):
        selection = bpy.context.active_object
        name = self.get_name(selection, "USP_")
        bpy.ops.mesh.primitive_uv_sphere_add(segments=8, ring_count=8, radius=rad, enter_editmode=False, align='WORLD', location=loc, rotation=rot)
        selection = bpy.context.active_object
        self.apply_material(selection)
        selection.name = name

    def execute(self, context):
        radius = self.get_radius()
        self.make_sphere(radius, self.location, self.rotation)
        return{'FINISHED'}


class UCPCollisionGenerator(UE4CollisionGenerator):
    bl_idname = "mesh.be_ucp"
    bl_label = "UCP Collision"
    bl_description = "Create cylinder collision for UE4"
    bl_options = {"REGISTER", "UNDO"}

    def __init__(self):
        self.bbox = self.get_bounding_box()
        self.dimensions = self.get_dimensions(self.bbox)
        # print("Dimensions are ", self.dimensions)
        self.radius = self.get_radius(self.dimensions)
        self.height = self.get_height(self.dimensions)
        self.axis_rotation = self.get_axis_rotation(self.dimensions)

    def get_dimensions(self, bbox):
        dimensions = []
        x_dim = abs(bbox[1].x - bbox[0].x)
        dimensions.append(x_dim)
        y_dim = abs(bbox[1].y - bbox[0].y)
        dimensions.append(y_dim)
        z_dim = abs(bbox[1].z - bbox[0].z)
        dimensions.append(z_dim)
        return dimensions

    def get_height(self, dimensions):
        h = max(dimensions)
        # print("Height is ", h)
        return h

    def get_radius(self, dimensions):
        sorted_dimensions = sorted(dimensions)
        # print(sorted_dimensions)
        
        # pythag
        a = sorted_dimensions[0] / 2.0
        b = sorted_dimensions[1] / 2.0
        r = math.sqrt(a*a+b*b)
        return r

    def get_axis_rotation(self, dimensions):
        axis = ['X', 'Y', 'Z']
        # print("Largets axis is ", axis[dimensions.index(max(dimensions))])
        rot_axis = axis[dimensions.index(max(dimensions))]

        if rot_axis == 'X':
            return (0, math.radians(90), 0)
        elif rot_axis == 'Y':
            return (math.radians(90), 0, 0)
        else:
            return(0, 0, 0)

    def create_cylinder(self, r, h, loc, rot):
        selection = bpy.context.active_object
        name = self.get_name(selection, "UCP_")
        bpy.ops.mesh.primitive_cylinder_add(vertices=8, radius = r, depth = h, enter_editmode=False, align='WORLD', location=loc, rotation=rot)
        selection = bpy.context.active_object
        selection.rotation_euler = self.axis_rotation
        self.apply_material(selection)
        selection.name = name

    def execute(self, context):
        self.create_cylinder(self.radius, self.height, self.location, self.rotation)
        return{'FINISHED'}