bl_info = {
    "name" : "Quality Of Life",
    "author" : "Almaas",
    "description" : "This addon might make your life better",
    "blender" : (2, 91, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "3D View"
}


from . import addon


def register():
    addon.register()


def unregister():
    addon.unregister()
