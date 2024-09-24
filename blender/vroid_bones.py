import bpy
bl_info = {
    "name": "VRM Swap Bone Names",
    "blender": (3, 4, 1),
    "category": "Object",
}


# Suffix slightly changed
# https://gist.githubusercontent.com/Ooseykins/ee55ca931ef91ef4e101a09fcb159977/raw/5dfeb0274ffbb0610f59bcfd0188487522041698/VRMSwapBoneNames.py

L_SIDE_PREFIX = "_L"
R_SIDE_PREFIX = "_R"
ORIG_PLACEHOLDER = "_d_"
ORIG_L_SIDE = "_L_"
ORIG_R_SIDE = "_R_"


class VRMSwapBoneNamesOperator(bpy.types.Operator):

    bl_idname = "object.vrmswapbonenames"
    bl_label = "VRM Swap Bone Names"
    bl_description = f"""Swap VRM style bone names to append {L_SIDE_PREFIX} and {
        R_SIDE_PREFIX} to all selected objects' vertex group names and bone names. Run this operator again to swap back to VRM style names with {ORIG_L_SIDE} and {ORIG_R_SIDE}"""
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        def replaceName(namedObject, mode):
            if ORIG_L_SIDE in namedObject.name and mode >= 0:
                namedObject.name = namedObject.name.replace(ORIG_L_SIDE, ORIG_PLACEHOLDER) + L_SIDE_PREFIX
                return 1
            elif ORIG_R_SIDE in namedObject.name and mode >= 0:
                namedObject.name = namedObject.name.replace(ORIG_R_SIDE, ORIG_PLACEHOLDER) + R_SIDE_PREFIX
                return 1
            elif ORIG_PLACEHOLDER in namedObject.name and L_SIDE_PREFIX in namedObject.name and mode <= 0:
                namedObject.name = namedObject.name.replace(ORIG_PLACEHOLDER, ORIG_L_SIDE).removesuffix(L_SIDE_PREFIX)
                return -1
            elif ORIG_PLACEHOLDER in namedObject.name and R_SIDE_PREFIX in namedObject.name and mode <= 0:
                namedObject.name = namedObject.name.replace(ORIG_PLACEHOLDER, ORIG_R_SIDE).removesuffix(R_SIDE_PREFIX)
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
