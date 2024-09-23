bl_info = {
    "name": "VRM Swap Bone Names",
    "blender": (3, 4, 1),
    "category": "Object",
}

import bpy

# Suffix slightly changed
# https://gist.githubusercontent.com/Ooseykins/ee55ca931ef91ef4e101a09fcb159977/raw/5dfeb0274ffbb0610f59bcfd0188487522041698/VRMSwapBoneNames.py

class VRMSwapBoneNamesOperator(bpy.types.Operator):
    
    bl_idname = "object.vrmswapbonenames"
    bl_label = "VRM Swap Bone Names"
    bl_description ="Swap VRM style bone names to append .L and .R to all selected objects' vertex group names and bone names. Run this operator again to swap back to VRM style names with _L_ and _R_"
    bl_options = {'REGISTER', 'UNDO'}
    
    def execute(self, context):
        def replaceName(namedObject, mode):
            if "_L_" in namedObject.name and mode >= 0:
                namedObject.name = namedObject.name.replace("_L_","_d_")+".L"
                return 1
            elif "_R_" in namedObject.name and mode >= 0:
                namedObject.name = namedObject.name.replace("_R_","_d_")+".R"
                return 1
            elif "_d_" in namedObject.name and ".L" in namedObject.name and mode <= 0:
                namedObject.name = namedObject.name.replace("_d_","_L_").removesuffix(".L")
                return -1
            elif "_d_" in namedObject.name and ".R" in namedObject.name and mode <= 0:
                namedObject.name = namedObject.name.replace("_d_","_R_").removesuffix(".R")
                return -1
            return mode
            
        mode = 0
        for target in bpy.context.selected_objects:
            v_groups = target.vertex_groups
            for vg in v_groups:
                mode = replaceName(vg, mode)
            if target.type == 'ARMATURE':
                for b in target.data.bones:
                    mode = replaceName(b, mode)
                    
        return {'FINISHED'}
    def invoke(self, context, event):
        return self.execute(context) 

def menu_func(self, context):
    self.layout.operator(VRMSwapBoneNamesOperator.bl_idname)

def register():
    bpy.utils.register_class(VRMSwapBoneNamesOperator)
    bpy.types.VIEW3D_MT_object.append(menu_func)

def unregister():
    bpy.utils.unregister_class(VRMSwapBoneNamesOperator)
    
if __name__ == "__main__":
    register()
