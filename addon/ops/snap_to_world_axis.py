import bpy
import bmesh
import mathutils


def snap_items(self, context):
    if context.mode == 'OBJECT':
        return [
            ('WORLD', 'World', 'Snap to world'),
            ('3DCURSOR', '3D Cursor', 'Snap to the 3D cursor'),
        ]

    elif context.mode == 'EDIT_MESH':
        return [
            ('WORLD', 'World', 'Snap to world'),
            ('OBJECT', 'Object', 'Snap to object origion'),
            ('3DCURSOR', '3D Cursor', 'Snap to the 3D cursor'),
        ]


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

    snap: bpy.props.EnumProperty(
        name='Snap To',
        description='What to snap to',
        items=snap_items,
        default=0,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'axes')
        layout.prop(self, 'snap')

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            if context.active_object is not None:
                return context.mode in {'OBJECT', 'EDIT_MESH'}

    def execute(self, context):
        active = context.active_object
        location = active.location

        if context.mode == 'OBJECT':
            if self.snap == 'WORLD':
                for index, value in enumerate(self.axes):
                    if value:
                        location[index] = 0

            elif self.snap == '3DCURSOR':
                cursor_location = context.scene.cursor.location

                for index, value in enumerate(self.axes):
                    if value:
                        location[index] = cursor_location[index]

        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(active.data)
            geo = bm.select_history.active

            if isinstance(geo, bmesh.types.BMVert):
                location = geo.co

            elif isinstance(geo, bmesh.types.BMEdge):
                location = (geo.verts[0].co + geo.verts[1].co) * 0.5

            elif isinstance(geo, bmesh.types.BMFace):
                location = geo.calc_center_median()

            space = active.matrix_world
            vec = -location

            if self.snap == 'WORLD':
                vec = -(space @ location)

            elif self.snap == 'OBJECT':
                space = mathutils.Matrix.Identity(4)

            elif self.snap == '3DCURSOR':
                cursor_location = context.scene.cursor.location
                vec = -((space @ location) - cursor_location)

            # Setting all the axes we don't wanna change to 0
            for index, value in enumerate(self.axes):
                if not value:
                    vec[index] = 0

            bmesh.ops.translate(bm, verts=bm.verts, vec=vec, space=space)
            bmesh.update_edit_mesh(active.data)

        return {'FINISHED'}
