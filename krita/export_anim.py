from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject
import imageio

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()

def export(node, i):
    if node.name().startswith("Group"):
        for child in node.childNodes():
            export(child, i)
    else:
        #if not node.animated() and i != 0:
        #    return
        #
        #if node.animated() and not node.hasKeyframeAtTime(i):
        #    return

        info = InfoObject()
        rect = QRect(sel.x(), sel.y(), sel.width(), sel.height())
        name = node.name()
        file = '{}/{}_{}.png'.format(folder, name, i)

        node.save(file, doc.xRes(), doc.yRes(), info, rect)
        print("Export layer {} at frame {}".format(name, i))

if sel and node:
    folder = QFileDialog.getExistingDirectory()
    if folder:
        #fps = doc.framesPerSecond()
        #images = []

        name = node.name()

        length = doc.animationLength()
        print("Exporting {} frames".format(length))
        for i in range(doc.playBackStartTime(), doc.playBackEndTime()):
            print("Exporting frame {}".format(i))
            doc.setCurrentTime(i)
            export(node, i)

            #images.append(imageio.imread(file))
        #final_file = '{}/{}.gif'.format(folder, node.name())
        #imageio.mimsave(final_file, images, 'GIF', fps=fps)
