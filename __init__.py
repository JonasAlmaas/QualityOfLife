bl_info = {
    "name" : "Quality Of Life",
    "author" : "Almaas",
    "description" : "This addon might just make your life that tad bit better",
    "blender" : (2, 91, 0),
    "version" : (0, 2, 0),
    "location" : "",
    "warning" : "",
    "category" : "3D View"
}


from . import addon


def register():
    addon.register()


def unregister():
    addon.unregister()
