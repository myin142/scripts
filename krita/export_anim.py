from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()

if sel and node:
    folder = QFileDialog.getExistingDirectory()
    rect = QRect(sel.x(), sel.y(), sel.width(), sel.height())

    info = InfoObject()
    for i in range(0, doc.animationLength()):
        file = '{}/{}_{}.png'.format(folder, node.name(), i)
        doc.setCurrentTime(i)
        node.save(file, doc.xRes(), doc.yRes(), info, rect)
