#################################################################
# Be Tools by Bruce Evans                                       #
# Created 4/6/2021                                              #
# brucein3d@gmail.com                                           #
#################################################################

import bpy
from mathutils import Vector


class DivideLattice(bpy.types.Operator):
    bl_label = "Lattice"
    bl_description = "Create a lattice deformer"
    bl_idname = "mesh.be_lattice"
    bl_options = {'REGISTER', 'UNDO'}

    def __init__(self, divisions):
        self.divisions = divisions
        self.current_selection = bpy.context.object.data

    def execute(self, context):
        try:

            #  TODO move pivots
            bpy.ops.mesh.be_lattice()

            if self.divisions == 2:
                bpy.context.object.data.points_u = 3
                bpy.context.object.data.points_v = 3
                bpy.context.object.data.points_w = 3
            elif self.divisions == 3:
                bpy.context.object.data.points_u = 4
                bpy.context.object.data.points_v = 4
                bpy.context.object.data.points_w = 4
            elif self.divisions == 4:
                bpy.context.object.data.points_u = 5
                bpy.context.object.data.points_v = 5
                bpy.context.object.data.points_w = 5
            # Add undo state
            bpy.ops.object.mode_set(mode = 'OBJECT')
        except TypeError:
            pass
        return {'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True

class Lattice_2(DivideLattice):
    bl_idname = "mesh.lattice_2"
    def __init__(self):
        DivideLattice.__init__(self, 2)

class Lattice_3(DivideLattice):
    bl_idname = "mesh.lattice_3"
    def __init__(self):
        DivideLattice.__init__(self, 3)

class Lattice_4(DivideLattice):
    bl_idname = "mesh.lattice_4"
    def __init__(self):
        DivideLattice.__init__(self, 4)


class Lattice(bpy.types.Operator):
    bl_idname = "mesh.be_lattice"
    bl_label = "Simple Lattice"
    bl_description = "Quickly create lattices based on the objects bounding box and position"
    bl_options = {'REGISTER', 'UNDO'}

    def get_bounding_box(self):

        selection = bpy.context.active_object

        if selection.mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')

        vertices = selection.data.vertices
        vert_positions = [vertex.co @ selection.matrix_world for vertex in vertices]
        self.rotation = bpy.data.objects[selection.name].rotation_euler
        self.location = bpy.data.objects[selection.name].location

        bb_min = Vector()
        bb_max = Vector()

        for axis in range(3):
            pos_list = [pos[axis] for pos in vert_positions]
            bb_max[axis] = max(pos_list)
            bb_min[axis] = min(pos_list)
            
        #  add location offset
        bb_max += self.location
        bb_min += self.location
        bounding_box = [bb_min, bb_max]

        return bounding_box

    def lattice_prep(self, context, selection):

        selection = bpy.context.active_object

        if selection.mode == 'EDIT':
            bpy.ops.object.mode_set(mode = 'OBJECT')

        # backup the original rotation
        # orig_rotation = selection.rotation_euler
        # print("Original rotation is ", orig_rotation)
        # zero out the rotation
        # selection.rotation_euler = (0, 0, 0)

        vertices = selection.data.vertices
        vert_positions = [vertex.co @ selection.matrix_world for vertex in vertices]
        self.obj_location = bpy.data.objects[selection.name].location

        minimum = Vector()
        maximum = Vector()
        
        for axis in range(3):
            pos_list = [pos[axis] for pos in vert_positions]
            maximum[axis] = max(pos_list)
            minimum[axis] = min(pos_list)
        center = (maximum + minimum) / 2
        dimensions = maximum - minimum

        self.lattice_location = self.obj_location + center

        # Create the lattice
        bpy.ops.object.add(type='LATTICE', enter_editmode=False, location=self.lattice_location)
        lattice = bpy.context.active_object
        lattice.data.use_outside = True
        lattice.name = selection.name + ".Lattice"
        lattice.data.interpolation_type_u = 'KEY_LINEAR'
        lattice.data.interpolation_type_v = 'KEY_LINEAR'
        lattice.data.interpolation_type_w = 'KEY_LINEAR'
        lattice.scale = dimensions
        lattice.rotation_euler = selection.rotation_euler
        bpy.context.view_layer.objects.active = selection
        bpy.ops.object.modifier_add(type='LATTICE')
        selection.modifiers["Lattice"].object = lattice
        selection.modifiers["Lattice"].vertex_group = "lattice_group"
        bpy.context.view_layer.objects.active = lattice

        # Apply original rotations TODO

        # print(selection.name)
        # print(lattice.name)

        # Deselect object, select lattice and make it active, switch to edit mode

        bpy.data.objects[selection.name].select_set(False)
        bpy.data.objects[lattice.name].select_set(True)
        bpy.ops.object.editmode_toggle()

    def apply_lattice(self, context, lattice):
        if context.mode == 'EDIT_MESH':
            bpy.ops.object.editmode_toggle()
        obj = bpy.data.objects[lattice.name[:-8]]
        bpy.data.objects[lattice.name].select_set(False)
        bpy.data.objects[obj.name].select_set(True)
        bpy.context.view_layer.objects.active = obj
        bpy.ops.object.modifier_apply(apply_as='DATA', modifier="Lattice")

		# Delete vertex group
        vg = obj.vertex_groups.get("lattice_group")
        if vg is not None:
            obj.vertex_groups.remove(vg)

		# Delete lattice
        bpy.data.objects[obj.name].select_set(False)
        bpy.data.objects[lattice.name].select_set(True)
        bpy.ops.object.delete()
        bpy.data.objects[obj.name].select_set(True)
        bpy.ops.object.editmode_toggle()

    def get_lattice(self,context, obj):
        lattice = obj.name + ".Lattice"
        if bpy.data.objects.get(lattice) is None:
            return False
        else:
            bpy.data.objects[obj.name].select_set(False)
            bpy.data.objects[lattice].select_set(True)
            context.view_layer.objects.active = bpy.data.objects[lattice]
            bpy.ops.object.editmode_toggle()
            return True

    def execute(self, context):
        selection = bpy.context.active_object
        if selection.name.endswith(".Lattice"):
            self.apply_lattice(context, selection)
            selection.location = self.obj_location
        elif self.get_lattice(context, selection):
            lattice = bpy.context.active_object
        else:
            self.lattice_prep(context, selection)
        return{'FINISHED'}

    @classmethod
    def poll(cls, context):
        if context.object is None:
            return False
        return True

bpy.utils.register_class(DivideLattice)
bpy.utils.register_class(Lattice)
bpy.utils.register_class(Lattice_2)
bpy.utils.register_class(Lattice_3)
bpy.utils.register_class(Lattice_4)
