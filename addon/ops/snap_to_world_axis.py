import bpy
import bmesh
import mathutils


class SnapToWorldAxis(bpy.types.Operator):
    bl_idname = 'qol.snap_to_world_axis'
    bl_label = 'Snap To World Axis'
    bl_description = 'Snap active vertex / edge / face to world axis'
    bl_options = {'REGISTER', 'UNDO'}

    axes: bpy.props.BoolVectorProperty(
        name='Axes',
        description='Which axes to snap to',
        size=3,
        subtype='XYZ',
        default=(False, False, True),
    )

    world: bpy.props.BoolProperty(
        name='Use World Space',
        description='Snap to world space axis',
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'axes')

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            if context.active_object is not None:
                return context.mode in {'OBJECT', 'EDIT_MESH'}

    def execute(self, context):
        active = context.active_object
        
        if context.mode == 'OBJECT':
            for index, value in enumerate(self.axes):
                if value:
                    active.location[index] = 0
        
        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(active.data)
            geo = bm.select_history.active

            if isinstance(geo, bmesh.types.BMVert):
                location = geo.co

            elif isinstance(geo, bmesh.types.BMEdge):
                location = (geo.verts[0].co + geo.verts[1].co) * 0.5

            elif isinstance(geo, bmesh.types.BMFace):
                location = geo.calc_center_median()

            else:
                location = active.location

            if self.world:
                space = active.matrix_world
            else:
                space=mathutils.Vector(3)

            vec = -(space @ location)

            for index, value in enumerate(self.axes):
                if not value:
                    vec[index] = 0

            bmesh.ops.translate(bm, verts=bm.verts, vec=vec, space=space)
            bmesh.update_edit_mesh(active.data)


        return {'FINISHED'}
