from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import DockWidget, Krita, InfoObject

ignore_start = "_" # ignore
group_start = ">" # export each child of the group
skip_group_name_end = "<" # don't add the group name to the prefix if name is ">GROUP<"
child_toggle_start = "@" # the parent will be exported with each child inside this group toggled

annotation_key = "myin_exporter_pref"

class Exporter(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exporter")

        mainWidget = QWidget(self)
        mainWidget.setLayout(QVBoxLayout())
        self.setWidget(mainWidget)

        form = QFormLayout()
        self.file_separator = QLineEdit(self.endpoint_widget)
        form.addRow("File separator", self.file_separator)

        exportBtn = QPushButton("Export", mainWidget)
        exportBtn.clicked.connect(self.exportDocument)
        mainWidget.layout().addWidget(exportBtn)

        self.loadPreferences()
        Krita.instance().notifier().applicationClosing.connect(self.savePreferences)
    
    @pyqtSlot()
    def savePreferences(self):
        doc = Krita.instance().activeDocument()
        data = self.file_separator.text()
        doc.setAnnotation(annotation_key, "Settings for the exporter plugin", QByteArray(data.encode()))
        print('Saved preferences', data)

    def loadPreferences(self):
        doc = Krita.instance().activeDocument()
        bytes = doc.annotation(annotation_key)

        if bytes and not bytes.isEmpty():
            data = bytes.toStdString()
            print('Loading preferences', data)

            self.file_separator.setText(data)

    def file_sep(self):
        return self.file_separator.text()
    
    def exportDocument(self):
        doc = Krita.instance().activeDocument()
        sel = doc.selection()
        node = doc.activeNode()

        self.rect = QRect(sel.x(), sel.y(), sel.width(), sel.height()) if sel else None
        self.doc = doc

        if node:
            self.folder = QFileDialog.getExistingDirectory()
            if self.folder:
                start = doc.playBackStartTime()
                end = doc.playBackEndTime() + 1
                length = end - start
                print("Exporting {} frames".format(length))

                for i in range(start, end):
                    doc.setCurrentTime(i)
                    doc.waitForDone()
                    self.export(node, i)

    def export(self, node, i, prefix = ""):
        node_name = node.name().strip()
        if not node.visible():
            return
        
        if node_name.startswith(group_start):
            for child in node.childNodes():
                new_prefix = prefix
                if not node_name.endswith(skip_group_name_end):
                    new_prefix += node_name[1:].strip()
                if new_prefix != "":
                    new_prefix += self.file_sep()
                self.export(child, i, new_prefix)
        elif not node_name.startswith(ignore_start):
            if not self.has_keyframe_at(node, i):
                #print("No keyframe at {} for {}".format(i, node_name))
                return
            
            toggle_group = self.get_toggle_group_child()
            if toggle_group == None:
                parts = [prefix + node_name]
                if i != 0 or self.has_keyframe_at(node, i + 1):
                    parts.append(i)
                file = '{}/{}.png'.format(self.folder, self.join_filename(parts))
                self.export_node(node, file)
                print("Export layer {} at frame {}".format(node_name, i))
            else:
                print("Start exporting toggle group for {}".format(prefix + node_name))
                for child in toggle_group.childNodes():
                    child.setVisible(False)
                
                toggle_name = toggle_group.name().strip()[1:]
                for child in toggle_group.childNodes():
                    child.setVisible(True)
                    
                    # TODO: support exporting frames?
                    n = self.join_filename([prefix, node_name, toggle_name + child.name().strip()])     
                    file = '{}/{}.png'.format(self.folder, n)
                    self.export_node(node, file)
                    print("Export layer {} at frame {}".format(node_name + child.name(), i))
    
    def get_toggle_group_child(self, node):
        if node.childNodes():
            for child in node.childNodes():
                if child.visible() and child.childNodes() and child.name().strip().startswith(child_toggle_start):
                    return child
        return None

    def has_keyframe_at(self, node, frame):
        children = node.childNodes()
        if children:
            for child in children:
                if self.has_keyframe_at(child, frame):
                    return True
            return False
        else:
            if node.animated():
                return node.hasKeyframeAtTime(frame)
            else:
                return frame == 0 and node.hasExtents()

    def export_node(self, node, filename):
        actual_rect = node.bounds() if self.rect is None else self.rect
        node.save(filename, self.doc.xRes(), self.doc.yRes(), InfoObject(), actual_rect)
        
    def join_filename(self, names):
        result = ""
        for i in range(0, len(names)):
            name = names[i].strip()
            if name == "": continue
            result += name
            if i != len(names) - 1:
                result += self.file_sep()
        return result

    # This function must exist
    def canvasChanged(self, canvas):
        pass