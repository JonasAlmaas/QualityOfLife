import bpy
import bmesh


class CheckerLoopSelect(bpy.types.Operator):
    bl_idname = 'qol.checker_loop_select'
    bl_label = 'Checker Loop Select'
    bl_description = 'Select every other loop'
    bl_options = {'REGISTER', 'UNDO'}

    @classmethod
    def poll(cls, context):
        if context.area.type == 'VIEW_3D':
            return context.mode == 'EDIT_MESH'
    
    def execute(self, context):
        active = context.active_object

        if context.mode == 'EDIT_MESH':
            bm = bmesh.from_edit_mesh(active.data)
            geo = bm.select_history.active

            # TODO, or maybe not
            if isinstance(geo, bmesh.types.BMVert):
                # What is even a vertex loop, and why do you want it again?
                pass

            elif isinstance(geo, bmesh.types.BMEdge):
                bpy.ops.mesh.select_all(action = 'DESELECT')

                for edge in bm.edges:
                    if edge == geo:
                        edge.select = True

                bpy.ops.mesh.loop_multi_select(ring=True)
                bpy.ops.mesh.select_nth()
                bpy.ops.mesh.loop_multi_select(ring=False)

            # TODO
            elif isinstance(geo, bmesh.types.BMFace):
                # bpy.ops.mesh.loop_multi_select(ring=True)     Only selects edge loops, doesn't look like face loops are a real thing, have to actualy use my brain on this one...
                pass

        return {'FINISHED'}
