from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject
import imageio

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()

if sel and node:
    folder = QFileDialog.getExistingDirectory()
    rect = QRect(sel.x(), sel.y(), sel.width(), sel.height())

    info = InfoObject()
    fps = doc.framesPerSecond()
    images = []
    for i in range(0, doc.animationLength()):
        file = '{}/{}_{}.png'.format(folder, node.name(), i)
        doc.setCurrentTime(i)
        node.save(file, doc.xRes(), doc.yRes(), info, rect)
        images.append(imageio.imread(file))
    final_file = '{}/{}.gif'.format(folder, node.name())
    imageio.mimsave(final_file, images, 'GIF', fps=fps)
