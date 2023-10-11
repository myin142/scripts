from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from krita import DockWidget, Krita, InfoObject

ignore_start = "_" # ignore
group_start = ">" # export each child of the group
skip_group_name_end = "<" # don't add the group name to the prefix if name is ">GROUP<"
child_toggle_start = "@" # the parent will be exported with each child inside this group toggled
skip_animation_start = "#" # skip this layer for checking if animation frame exist
mask_name = "_mask" # using mask size for export

annotation_key = "myin_exporter_pref"

class Exporter(DockWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Exporter")

        mainWidget = QWidget(self)
        mainWidget.setLayout(QVBoxLayout())
        self.setWidget(mainWidget)

        formWidget = QWidget(mainWidget)
        form = QFormLayout()

        self.file_separator = QLineEdit(formWidget)
        self.file_separator.setText("_")
        form.addRow("File separator", self.file_separator)

        self.skip_single_frame_number = QCheckBox()
        form.addRow("Skip single frame number", self.skip_single_frame_number)

        formWidget.setLayout(form)
        mainWidget.layout().addWidget(formWidget)

        exportBtn = QPushButton("Export", mainWidget)
        exportBtn.clicked.connect(self.exportDocument)
        mainWidget.layout().addWidget(exportBtn)

        notifier = Krita.instance().notifier()
        notifier.imageCreated.connect(self.loadPreferences)
        notifier.applicationClosing.connect(self.savePreferences)

    @pyqtSlot()
    def savePreferences(self):
        doc = Krita.instance().activeDocument()
        data = self.file_separator.text()
        doc.setAnnotation(annotation_key, "Settings for the exporter plugin", QByteArray(data.encode()))
        print('Saved preferences', data)

    @pyqtSlot()
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

        self.sel = QRect(sel.x(), sel.y(), sel.width(), sel.height()) if sel else None
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

                    if self.skip_single_frame_number.isChecked():
                        break

    def export(self, node, i, prefix = ""):
        node_name = node.name().strip()
        if not node.visible():
            return

        if node_name.startswith(group_start):
            for child in node.childNodes():
                new_prefix = prefix
                if not node_name.endswith(skip_group_name_end):
                    new_prefix += node_name[1:].strip()
                    new_prefix += self.file_sep()
                self.export(child, i, new_prefix)
        elif not node_name.startswith(ignore_start):
            if not self.has_keyframe_at(node, i):
                return

            toggle_group, mask = self.collect_info(node)

            if mask != None and mask.visible():
                mask.setVisible(False)
                self.doc.refreshProjection()

            export_rect = self.get_export_rect(node, mask)

            # Remove seperator if node name is empty
            if node_name == "":
                count = len(self.file_sep()) * -1
                prefix = prefix[:count]

            if toggle_group == None:
                parts = [prefix + node_name]
                if i != 0 or not self.skip_single_frame_number.isChecked(): #or self.has_keyframe_at(node, i + 1):
                    parts.append(i)
                file = '{}/{}.png'.format(self.folder, self.join_filename(parts))
                self.export_node(export_rect, node, file)
                print("Export layer {} at frame {}".format(node_name, i))
            else:
                print("Start exporting toggle group for {}".format(prefix + node_name))
                for child in toggle_group.childNodes():
                    child.setVisible(False)
                self.doc.waitForDone()

                toggle_name = toggle_group.name().strip()[1:]
                for child in toggle_group.childNodes():
                    child.setVisible(True)
                    self.doc.refreshProjection() # this is costly

                    # TODO: support exporting frames?
                    n = self.join_filename([prefix, node_name, toggle_name + child.name().strip()])
                    file = '{}/{}.png'.format(self.folder, n)
                    self.export_node(export_rect, node, file)
                    print("Export layer {} at frame {}".format(node_name + child.name(), i))
                    child.setVisible(False)

    def collect_info(self, node):
        toggle_group = None
        mask = None

        # Hopefully we can save some time if we combine the first iteration of child nodes
        if node.childNodes():
            for child in node.childNodes():
                name = child.name().strip()

                if toggle_group == None and child.visible() and child.childNodes() and name.startswith(child_toggle_start):
                    toggle_group = child

                if mask == None and name == mask_name:
                    mask = child

        if mask == None:
            parent = node.parentNode()
            if parent:
                for sibling in parent.childNodes():
                    if sibling == node: continue

                    if sibling.name().strip() == mask_name:
                        mask = sibling
                        break

        return toggle_group, mask

    def get_export_rect(self, node, mask):
        export_rect = self.sel
        if export_rect == None:
            if mask == None:
                export_rect = node.bounds()
            else:
                export_rect = mask.bounds()
        return export_rect

    def has_keyframe_at(self, node, frame):
        children = node.childNodes()
        if children:
            if not node.name().startswith(skip_animation_start):
                for child in children:
                    if self.has_keyframe_at(child, frame):
                        return True
            return False
        else:
            if node.animated() and not node.name().startswith(skip_animation_start):
                return node.hasKeyframeAtTime(frame)
            else:
                return frame == 0 and node.hasExtents()

    def export_node(self, rect, node, filename):
        node.save(filename, self.doc.xRes(), self.doc.yRes(), InfoObject(), rect)

    def join_filename(self, names):
        result = ""
        for i in range(0, len(names)):
            name = str(names[i]).strip()
            if name == "": continue
            result += name
            if i != len(names) - 1:
                result += self.file_sep()
        return result

    # This function must exist
    def canvasChanged(self, canvas):
        pass
