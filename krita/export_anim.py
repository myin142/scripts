from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject
import imageio

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()
info = InfoObject()
rect = QRect(sel.x(), sel.y(), sel.width(), sel.height()) if sel else doc.bounds()

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
    if node_name.startswith(">"):
        for child in node.childNodes():
            export(child, i, node_name[1:] + "_")
    else:
        if not has_keyframe_at(node, i):
            return

        name = prefix + node.name()
        file = '{}/{}_{}.png'.format(folder, name, i)

        node.save(file, doc.xRes(), doc.yRes(), info, rect)
        print("Export layer {} at frame {}".format(name, i))

if node:
    folder = QFileDialog.getExistingDirectory()
    if folder:
        #fps = doc.framesPerSecond()
        #images = []

        name = node.name()
        length = doc.animationLength()
        print("Exporting {} frames".format(length))

        for i in range(doc.playBackStartTime(), doc.playBackEndTime() + 1):
            print("Exporting frame {}".format(i))
            doc.setCurrentTime(i)
            export(node, i)

            #images.append(imageio.imread(file))
        #final_file = '{}/{}.gif'.format(folder, node.name())
        #imageio.mimsave(final_file, images, 'GIF', fps=fps)
