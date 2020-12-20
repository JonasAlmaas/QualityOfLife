import bpy
from . import checker_loop_select
from . import snap_to_world_axis



# Menu containing all tools
class VIEW3D_MENU_quality_of_life(bpy.types.Menu):
    bl_label = "Quality Of Life"

    def draw(self, context):
        layout = self.layout
        layout.operator("qol.checker_loop_select")
        layout.operator("qol.snap_to_world_axis")


# Draw function for menus
def menu_func(self, context):
    self.layout.menu("VIEW3D_MENU_quality_of_life")
    self.layout.separator()


classes = (
    VIEW3D_MENU_quality_of_life,
    checker_loop_select.CheckerLoopSelect,
    snap_to_world_axis.SnapToWorldAxis,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.prepend(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.prepend(menu_func)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.types.VIEW3D_MT_object_context_menu.remove(menu_func)
