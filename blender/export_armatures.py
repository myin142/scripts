import bpy
import os

# ==============================================
# CONFIGURATION - DEFINE YOUR COLLECTIONS HERE
# ==============================================

COLLECTION_MAP = {
    "HairFront": r"",
    "HairSide": r"",
    "HairBack": r"",
}

# ==============================================
# SCRIPT LOGIC
# ==============================================

def ensure_output_folder(folder_path):
    """Create output folder if it doesn't exist"""
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"  📁 Created folder: {folder_path}")
        return True
    print(f"  📁 Folder exists: {folder_path}")
    return False

def get_objects_in_collection(collection_name):
    """Get all objects in a collection"""
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"  ❌ Collection '{collection_name}' NOT FOUND!")
        return []
    
    objects = list(collection.all_objects)
    print(f"  ✅ Found {len(objects)} objects in collection '{collection_name}'")
    
    if objects:
        print(f"  Objects in collection:")
        for obj in objects:
            print(f"    - {obj.name} (Type: {obj.type})")
    else:
        print(f"  ⚠️ Collection is EMPTY!")
    
    return objects

def find_armature_with_meshes(objects):
    """Find armatures and their child meshes"""
    armature_groups = []
    
    armatures = [obj for obj in objects if obj.type == 'ARMATURE']
    meshes = [obj for obj in objects if obj.type == 'MESH']
    
    print(f"\n  🔍 Analyzing objects:")
    print(f"    Armatures found: {len(armatures)}")
    print(f"    Meshes found: {len(meshes)}")
    
    if not armatures:
        print(f"  ⚠️ No armatures found in this collection!")
        return []
    
    if not meshes:
        print(f"  ⚠️ No meshes found in this collection!")
        return []
    
    # For each armature, find parented meshes
    for armature in armatures:
        child_meshes = []
        
        print(f"\n  🔍 Processing armature: {armature.name}")
        
        # Method 1: Check direct parenting
        for mesh in meshes:
            parent = mesh.parent
            while parent:
                if parent == armature:
                    child_meshes.append(mesh)
                    print(f"    ✅ Found parented mesh: {mesh.name}")
                    break
                parent = parent.parent
        
        # Method 2: Check armature modifiers
        for mesh in meshes:
            if mesh not in child_meshes and mesh.modifiers:
                for modifier in mesh.modifiers:
                    if modifier.type == 'ARMATURE' and modifier.object == armature:
                        child_meshes.append(mesh)
                        print(f"    ✅ Found mesh with armature modifier: {mesh.name}")
                        break
        
        # Method 3: Check vertex groups
        for mesh in meshes:
            if mesh not in child_meshes and mesh.vertex_groups:
                if armature.data.bones:
                    bone_names = [bone.name for bone in armature.data.bones]
                    for vgroup in mesh.vertex_groups:
                        if vgroup.name in bone_names:
                            child_meshes.append(mesh)
                            print(f"    ✅ Found mesh with matching vertex groups: {mesh.name}")
                            break
        
        if child_meshes:
            armature_groups.append((armature, child_meshes))
            print(f"  ✅ Armature {armature.name} has {len(child_meshes)} mesh(es)")
        else:
            print(f"  ⚠️ Armature {armature.name} has NO meshes attached!")
    
    return armature_groups

def export_armature_group(armature, meshes, output_folder):
    """Export a single armature with its meshes to FBX"""
    print(f"\n  📤 Exporting: {armature.name}")
    
    # Select only the armature and its meshes
    bpy.ops.object.select_all(action='DESELECT')
    
    armature.select_set(True)
    for mesh in meshes:
        mesh.select_set(True)
    
    # Ensure we have the armature as active object
    bpy.context.view_layer.objects.active = armature
    
    # Build export filename
    filename = f"{armature.name}.fbx"
    filepath = os.path.join(output_folder, filename)
    print(f"    Export path: {filepath}")
    
    # Export to FBX with ONLY parameters from the official documentation
    try:
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,  # Export only selected objects
            object_types={'ARMATURE', 'MESH'},  # Only export armatures and meshes
            use_mesh_modifiers=True,  # Apply modifiers
            mesh_smooth_type='OFF',  # No smoothing
            use_tspace=False,  # Don't add tangent space
            add_leaf_bones=False,  # Don't add leaf bones
            bake_anim=False,  # THIS DISABLES ANIMATIONS - Correct parameter name
            bake_anim_use_nla_strips=False,  # Don't use NLA strips
            bake_anim_use_all_actions=False,  # Don't use all actions
            bake_anim_force_startend_keying=False,  # Don't force start/end keying
            global_scale=1.0,  # Keep original scale
            use_metadata=True  # Include metadata
        )
        print(f"    ✅ Successfully exported: {filename}")
        return True
    except Exception as e:
        print(f"    ❌ Error exporting {filename}: {str(e)}")
        print(f"    💡 Check that you're using the correct Blender version")
        return False

def process_collection(collection_name, output_folder):
    """Process a single collection and export all armatures"""
    print(f"\n{'='*60}")
    print(f"📦 Processing Collection: '{collection_name}'")
    print(f"📁 Output Folder: {output_folder}")
    print(f"{'='*60}")
    
    # Ensure output folder exists
    ensure_output_folder(output_folder)
    
    # Get objects from collection
    objects = get_objects_in_collection(collection_name)
    if not objects:
        print(f"  ❌ No objects found in collection. Skipping.")
        return 0
    
    # Find armatures with their meshes
    armature_groups = find_armature_with_meshes(objects)
    
    if not armature_groups:
        print(f"\n  ❌ No armature-mesh groups found. Skipping.")
        return 0
    
    print(f"\n  Found {len(armature_groups)} armature-mesh groups to export")
    print(f"  {'-'*56}")
    
    # Export each armature group
    exported_count = 0
    for armature, meshes in armature_groups:
        if meshes:
            if export_armature_group(armature, meshes, output_folder):
                exported_count += 1
        else:
            print(f"    ⚠️ Skipping {armature.name} - No meshes found")
    
    print(f"  {'-'*56}")
    print(f"  ✅ Collection complete: {exported_count}/{len(armature_groups)} exported")
    return exported_count

def main():
    """Main execution function"""
    print("\n" + "="*60)
    print("🎯 MULTI-COLLECTION FBX ARMATURE EXPORTER")
    print("="*60)
    print(f"📋 Collections to process: {len(COLLECTION_MAP)}")
    
    # Print current scene info
    print(f"\n📊 Current Scene: {bpy.context.scene.name}")
    print(f"📊 Total collections in file: {len(bpy.data.collections)}")
    print(f"📊 Total objects in file: {len(bpy.data.objects)}")
    
    # List available collections
    print("\n📋 Available collections in this file:")
    for col in bpy.data.collections:
        print(f"    - {col.name}")
    
    if not COLLECTION_MAP:
        print("❌ No collections defined in COLLECTION_MAP!")
        return
    
    total_exported = 0
    total_armatures = 0
    
    # Process each collection in the map
    for collection_name, output_folder in COLLECTION_MAP.items():
        exported = process_collection(collection_name, output_folder)
        
        # Count total armatures processed
        objects = get_objects_in_collection(collection_name)
        if objects:
            armatures = [obj for obj in objects if obj.type == 'ARMATURE']
            total_armatures += len(armatures)
        
        total_exported += exported
    
    # Final summary
    print("\n" + "="*60)
    print("📊 EXPORT SUMMARY")
    print("="*60)
    print(f"✅ Total collections processed: {len(COLLECTION_MAP)}")
    print(f"✅ Total armatures found: {total_armatures}")
    print(f"✅ Total armatures exported: {total_exported}")
    
    if total_exported == 0:
        print("\n⚠️ NOTHING WAS EXPORTED!")
        print("\n🔍 DEBUGGING CHECKLIST:")
        print("  1. Do the collections exist in your Blender file?")
        print("  2. Does each collection contain an armature AND meshes?")
        print("  3. Are the meshes parented to the armatures?")
        print("     - Select mesh, Shift+Select armature, Ctrl+P > Armature Deform")
        print("  4. Are the collection names spelled exactly the same?")
    
    print("\n📁 Output folders used:")
    for collection_name, output_folder in COLLECTION_MAP.items():
        print(f"    • {collection_name}: {output_folder}")
    print("="*60 + "\n")

# ==============================================
# RUN THE SCRIPT
# ==============================================

if __name__ == "__main__":
    main()
