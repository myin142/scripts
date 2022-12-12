from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import InfoObject

doc = Krita.instance().activeDocument()
sel = doc.selection()
node = doc.activeNode()

if node and node.childNodes():
    folder = QFileDialog.getExistingDirectory()
    
    if folder:
        name = node.name()
        info = InfoObject()
        children = node.childNodes()

        rect = QRect(sel.x(), sel.y(), sel.width(), sel.height()) if sel else doc.bounds()
        for i in range(0, len(children)):
            child = children[i]
            file = '{}/{}_{}.png'.format(folder, name, i)
            print('Exporting Layer {} to {}'.format(i, file))
            child.save(file, doc.xRes(), doc.yRes(), info, rect)

        