from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject

ignore_start = "_" # ignore
group_start = ">" # export each child of the group
skip_group_name_end = "<" # don't add the group name to the prefix if name is ">GROUP<"
child_toggle_start = "@" # the parent will be exported with each child inside this group toggled

filename_sep = "_"

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()
info = InfoObject()
rect = QRect(sel.x(), sel.y(), sel.width(), sel.height()) if sel else None

def has_keyframe_at(node, frame):
    children = node.childNodes()
    if children:
        for child in children:
            if has_keyframe_at(child, frame):
                return True
        return False
    else:
        if node.animated():
            return node.hasKeyframeAtTime(frame)
        else:
            return frame == 0 and node.hasExtents()

def export_node(node, filename, name = node.name()):
    actual_rect = node.bounds() if rect is None else rect
    node.save(filename, doc.xRes(), doc.yRes(), info, actual_rect)
    print("Export layer {} at frame {}".format(name, i))

def create_filename(name, i):
    file = '{}/{}{}{}.png'.format(folder, name, filename_sep, i)
    
    if i == 0 and not has_keyframe_at(node, i + 1):
        file = '{}/{}.png'.format(folder, name)
        
    return file    
    
def join_filename(names):
    result = ""
    for i in range(0, len(names)):
        name = names[i].strip()
        if name == "": continue
        result += name
        if i != len(names) - 1:
            result += filename_sep
    return result

def export(node, i, prefix = ""):
    node_name = node.name().strip()
    if not node.visible():
        return
    
    if node_name.startswith(group_start):
        for child in node.childNodes():
            new_prefix = prefix
            if not node_name.endswith(skip_group_name_end):
                new_prefix += node_name[1:].strip()
            if new_prefix != "":
                new_prefix += filename_sep
            export(child, i, new_prefix)
    elif not node_name.startswith(ignore_start):
        if not has_keyframe_at(node, i):
            #print("No keyframe at {} for {}".format(i, node_name))
            return
        
        toggle_group = None
        if node.childNodes():
            for child in node.childNodes():
                if child.visible() and child.childNodes() \
                    and child.name().strip().startswith(child_toggle_start):
                    toggle_group = child

        if toggle_group == None:
            file = create_filename(prefix + node_name, i)
            export_node(node, file)
        else:
            print("Start exporting toggle group for {}".format(prefix + node_name))
            for child in toggle_group.childNodes():
                child.setVisible(False)
             
            toggle_name = toggle_group.name().strip()[1:]
            for child in toggle_group.childNodes():
                child.setVisible(True)
                
                n = join_filename([prefix, node_name, toggle_name + child.name().strip()])     
                file = create_filename(n, i)
                export_node(node, file, node.name() + child.name())



if node:
    folder = QFileDialog.getExistingDirectory()
    if folder:
        name = node.name()
        start = doc.playBackStartTime()
        end = doc.playBackEndTime() + 1
        length = end - start
        print("Exporting {} frames".format(length))

        for i in range(start, end):
            doc.setCurrentTime(i)
            doc.waitForDone()
            export(node, i)
