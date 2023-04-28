from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject
import imageio

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

def export(node, i, prefix = ""):
    node_name = node.name().strip()
    if not node.visible():
        return
    
    if node_name.startswith(">"):
        for child in node.childNodes():
            new_prefix = prefix
            if not node_name.endswith("<"):
                new_prefix += node_name[1:].strip()
            if new_prefix != "":
                new_prefix += "_"
            export(child, i, new_prefix)
    elif not node_name.startswith("_"):
        if not has_keyframe_at(node, i):
            #print("No keyframe at {} for {}".format(i, node_name))
            return

        name = prefix + node.name()
        file = '{}/{}_{}.png'.format(folder, name, i)

        actual_rect = node.bounds() if rect is None else rect
        node.save(file, doc.xRes(), doc.yRes(), info, actual_rect)
        print("Export layer {} at frame {}".format(name, i))

if node:
    folder = QFileDialog.getExistingDirectory()
    if folder:
        #fps = doc.framesPerSecond()
        #images = []

        name = node.name()
        start = doc.playBackStartTime()
        end = doc.playBackEndTime() + 1
        length = end - start
        print("Exporting {} frames".format(length))

        for i in range(start, end):
            #print("Exporting frame {}".format(i))
            doc.setCurrentTime(i)
            doc.waitForDone()
            export(node, i)

            #images.append(imageio.imread(file))
        #final_file = '{}/{}.gif'.format(folder, node.name())
        #imageio.mimsave(final_file, images, 'GIF', fps=fps)
