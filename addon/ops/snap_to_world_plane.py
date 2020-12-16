
import bpy
import bmesh
import mathutils


class SnapToWorldPlane(bpy.types.Operator):
    bl_idname = 'qol.snap_to_world_plane'
    bl_label = 'Snap To World Plane'
    bl_description = 'Snap active vertex / edge / face to world plane'
    bl_options = {'REGISTER', 'UNDO'}

    plane: bpy.props.EnumProperty(
        name='Plane',
        description='Which world plane to snap to',
        items=[
            ('XY', 'XY', 'The XY world plane'),
            ('XZ', 'XZ', 'The XZ world plane'),
            ('YZ', 'YZ', 'The YZ world plane'),
        ],
        default='XY',
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'plane')

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            if context.active_object is not None:
                return context.mode in {'OBJECT', 'EDIT_MESH'}

    def execute(self, context):
        active = context.active_object
        position = active.location

        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(active.data)
            geo = bm.select_history.active

            # If the active geo is a vertex
            if isinstance(geo, bmesh.types.BMVert):
                position = geo.co

            # If the active geo is an edge
            elif isinstance(geo, bmesh.types.BMEdge):
                position = (geo.verts[0].co + geo.verts[1].co) * 0.5

            # If the active is a face
            elif isinstance(geo, bmesh.types.BMFace):
                position = geo.calc_center_median()

        context.scene.cursor.location = position

        return {'FINISHED'}
