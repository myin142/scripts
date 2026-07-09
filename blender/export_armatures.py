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
    return False

def unhide_all_in_collection(collection):
    """Unhide all objects in a collection and its children"""
    print(f"  🔓 Unhiding objects in collection: {collection.name}")
    
    # Unhide the collection itself
    collection.hide_viewport = False
    collection.hide_render = False
    
    # Unhide all objects in the collection
    for obj in collection.all_objects:
        obj.hide_viewport = False
        obj.hide_render = False
        obj.hide_select = False
        
        # If it's in a hidden collection, we need to handle that too
        for col in obj.users_collection:
            col.hide_viewport = False
            col.hide_render = False
    
    # Also unhide any nested collections
    for child_col in collection.children:
        unhide_all_in_collection(child_col)
    
    print(f"  ✅ All objects in {collection.name} are now visible")

def get_objects_in_collection(collection_name, unhide=True):
    """Get all objects in a collection, optionally unhiding them first"""
    collection = bpy.data.collections.get(collection_name)
    if not collection:
        print(f"  ❌ Collection '{collection_name}' NOT FOUND!")
        return []
    
    # Unhide everything if requested
    if unhide:
        unhide_all_in_collection(collection)
    
    # Get all objects in the collection (including nested)
    objects = list(collection.all_objects)
    print(f"  ✅ Found {len(objects)} objects in collection '{collection_name}'")
    
    # Detailed debug info with visibility status
    print(f"\n  📋 Detailed object list:")
    for obj in objects:
        print(f"    - {obj.name}")
        print(f"        Type: {obj.type}")
        print(f"        Visible: Viewport={not obj.hide_viewport}, Render={not obj.hide_render}, Select={not obj.hide_select}")
        if obj.type == 'MESH':
            print(f"        Parent: {obj.parent.name if obj.parent else 'None'}")
            if obj.modifiers:
                print(f"        Modifiers: {[mod.type for mod in obj.modifiers]}")
            if obj.vertex_groups:
                print(f"        Vertex Groups: {len(obj.vertex_groups)}")
        elif obj.type == 'ARMATURE':
            print(f"        Bones: {len(obj.data.bones)}")
        print()
    
    return objects

def find_armature_with_meshes_robust(objects, collection_name):
    """
    Find armatures and their meshes using multiple methods.
    Includes handling for hidden objects.
    """
    armature_groups = []
    
    # Separate armatures and meshes (including hidden ones)
    armatures = [obj for obj in objects if obj.type == 'ARMATURE']
    meshes = [obj for obj in objects if obj.type == 'MESH']
    
    print(f"\n  🔍 Analyzing objects in {collection_name}:")
    print(f"    Armatures found: {len(armatures)}")
    print(f"    Meshes found: {len(meshes)}")
    
    if not armatures:
        print(f"  ⚠️ No armatures found in this collection!")
        all_armatures = [obj for obj in bpy.data.objects if obj.type == 'ARMATURE']
        if all_armatures:
            print(f"  ℹ️ Found {len(all_armatures)} armatures in the scene but none in this collection")
            print(f"     Armatures in scene: {[a.name for a in all_armatures]}")
        return []
    
    if not meshes:
        print(f"  ⚠️ No meshes found in this collection!")
        all_meshes = [obj for obj in bpy.data.objects if obj.type == 'MESH']
        if all_meshes:
            print(f"  ℹ️ Found {len(all_meshes)} meshes in the scene but none in this collection")
            print(f"     Meshes in scene: {[m.name for m in all_meshes[:5]]}...")
        return []
    
    # For each armature, find its meshes using multiple methods
    for armature in armatures:
        child_meshes = []
        matching_methods = []
        
        print(f"\n  🔍 Searching for meshes belonging to: {armature.name}")
        
        # METHOD 1: Direct parent-child relationship (including hidden)
        for mesh in meshes:
            parent = mesh.parent
            while parent:
                if parent == armature:
                    child_meshes.append(mesh)
                    matching_methods.append(f"  ✅ {mesh.name} - Direct parent (visible: {not mesh.hide_viewport})")
                    break
                parent = parent.parent

        # REMOVED METHOD 4 - The fallback that was causing your issue
        # Now if no meshes are found, we don't assign any
        
        # Print matching results
        if matching_methods:
            print(f"  Found {len(child_meshes)} mesh(es) for {armature.name}:")
            for method in matching_methods:
                print(method)
        else:
            print(f"  ⚠️ No meshes found for {armature.name}")
            print(f"  💡 Suggestions:")
            print(f"     1. Select mesh, Shift+Select armature, Ctrl+P > Armature Deform")
            print(f"     2. Add Armature modifier to mesh")
            print(f"     3. Make sure vertex groups match bone names")
            print(f"     4. Make sure objects are not hidden in the viewport")
            print(f"     5. Check if meshes are in the correct collection")
        
        if child_meshes:
            armature_groups.append((armature, child_meshes))
    
    return armature_groups

def export_armature_group(armature, meshes, output_folder):
    """Export a single armature with its meshes to FBX"""
    print(f"\n  📤 Exporting: {armature.name} with {len(meshes)} mesh(es)")
    
    # Make sure objects are visible and selectable before export
    armature.hide_viewport = False
    armature.hide_select = False
    for mesh in meshes:
        mesh.hide_viewport = False
        mesh.hide_select = False
    
    # Select only the armature and its meshes
    bpy.ops.object.select_all(action='DESELECT')
    
    armature.select_set(True)
    for mesh in meshes:
        mesh.select_set(True)
        print(f"    Selected mesh: {mesh.name}")
    
    # Ensure we have the armature as active object
    bpy.context.view_layer.objects.active = armature
    
    # Build export filename
    filename = f"{armature.name}.fbx"
    filepath = os.path.join(output_folder, filename)
    print(f"    Export path: {filepath}")
    
    # Export to FBX
    try:
        bpy.ops.export_scene.fbx(
            filepath=filepath,
            use_selection=True,
            object_types={'ARMATURE', 'MESH'},
            apply_scale_options='FBX_SCALE_ALL',
            use_mesh_modifiers=True,
            bake_anim=False,
        )
        print(f"    ✅ Successfully exported: {filename}")
        return True
    except Exception as e:
        print(f"    ❌ Error exporting {filename}: {str(e)}")
        return False

def process_collection(collection_name, output_folder):
    """Process a single collection and export all armatures"""
    print(f"\n{'='*60}")
    print(f"📦 Processing Collection: '{collection_name}'")
    print(f"📁 Output Folder: {output_folder}")
    print(f"{'='*60}")
    
    # Ensure output folder exists
    ensure_output_folder(output_folder)
    
    # Get objects from collection (and unhide everything)
    objects = get_objects_in_collection(collection_name, unhide=True)
    if not objects:
        print(f"  ❌ No objects found in collection. Skipping.")
        return 0
    
    # Find armatures with their meshes
    armature_groups = find_armature_with_meshes_robust(objects, collection_name)
    
    if not armature_groups:
        print(f"\n  ❌ No armature-mesh groups found. Skipping.")
        print(f"  💡 Make sure your meshes are properly linked to armatures.")
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
    print("🎯 HIDDEN-OBJECT AWARE ARMATURE-MESH FBX EXPORTER")
    print("="*60)
    print(f"📋 Collections to process: {len(COLLECTION_MAP)}")
    
    # Store original visibility state (optional - if you want to restore later)
    # We're not restoring to avoid complexity, but could be added
    
    # Print current scene info
    print(f"\n📊 Current Scene: {bpy.context.scene.name}")
    print(f"📊 Total collections in file: {len(bpy.data.collections)}")
    print(f"📊 Total objects in file: {len(bpy.data.objects)}")
    
    # List available collections with visibility info
    print("\n📋 Available collections in this file:")
    for col in bpy.data.collections:
        vis_status = "Visible" if not col.hide_viewport else "HIDDEN"
        print(f"    - {col.name} ({vis_status})")
    
    if not COLLECTION_MAP:
        print("❌ No collections defined in COLLECTION_MAP!")
        return
    
    total_exported = 0
    total_armatures = 0
    
    # Process each collection in the map
    for collection_name, output_folder in COLLECTION_MAP.items():
        exported = process_collection(collection_name, output_folder)
        
        # Count total armatures processed
        objects = get_objects_in_collection(collection_name, unhide=False)
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
        print("  1. Are the collections visible in the Outliner?")
        print("     - The script tries to unhide them, but check manually")
        print("  2. Does each collection contain an armature AND meshes?")
        print("     - Check the detailed output above")
        print("  3. Are the meshes properly linked to the armatures?")
        print("     - Parent (Ctrl+P), Armature Modifier, or Vertex Groups")
        print("  4. Are the collection names spelled exactly the same?")
        print("     - Your collections:", list(COLLECTION_MAP.keys()))
        print("     - Available collections:", [col.name for col in bpy.data.collections])
        print("  5. Are the objects hidden in the viewport?")
        print("     - Check the eye icon in Outliner")
    
    print("\n📁 Output folders used:")
    for collection_name, output_folder in COLLECTION_MAP.items():
        print(f"    • {collection_name}: {output_folder}")
    print("="*60 + "\n")

# ==============================================
# RUN THE SCRIPT
# ==============================================

if __name__ == "__main__":
    main()