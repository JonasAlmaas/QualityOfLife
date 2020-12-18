import bpy
from . import snap_to_world_axis


classes = (
    snap_to_world_axis.SnapToWorldAxis,
)


def register():
    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
