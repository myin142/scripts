import bpy

ROOT = ''
COLLECTION = 'Objects'

# -----------------------------------

bpy.ops.object.mode_set(mode = 'OBJECT')

for obj in bpy.data.collections[COLLECTION].objects:
    if obj == None: continue

    bpy.ops.object.select_all(action='DESELECT')
    obj.hide_set(state=False)
    obj.select_set(state=True)
    
    bpy.ops.export_scene.gltf(
        filepath=ROOT + obj.name + '.gltf',
        export_format="GLTF_SEPARATE",
        check_existing=False,
        use_selection=True,
        export_import_convert_lighting_mode='COMPAT',
        export_apply=True,
        filter_glob="*.gltf"
    )

