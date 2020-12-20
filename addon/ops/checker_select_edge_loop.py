import bpy


class CheckerSelectEdgeLoop(bpy.types.Operator):
    bl_idname = 'qol.checker_select_edge_loop'
    bl_label = 'Checker Select Edge Loop'
    bl_description = 'Select every other edge loop'
    bl_options = {'REGISTER', 'UNDO'}

    invert: bpy.props.BoolProperty(
        name='Invert Selection',
        description='If you want to invert the selction or not',
        default=True,
    )

    def draw(self, context):
        layout = self.layout
        layout.prop(self, 'invert')

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        if context.mode == 'EDIT_MESH':
            pass

        return {'FINISHED'}
