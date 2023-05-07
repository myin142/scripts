from krita import *
#w = Krita.resources('workspace')['Animation']
#x = [method_name for method_name in dir(w) if callable(getattr(w, method_name))]
#print(x)


#object_methods = [method_name for method_name in dir(mw) if callable(getattr(mw, method_name))]
#print(object_methods)

#mw = Krita.activeWindow().qwindow()
#mw.restoreWorkspaceState()

grayscale_node = "_grayscale"

class ToggleDockerExtension(Extension):
    def __init__(self, parent):
        super().__init__(parent)

    def setup(self):
        pass

    def createActions(self, window):
        anim = window.createAction("toggle_docker_animation", "Toggle Animation Docker", "tools/scripts")
        anim.triggered.connect(self.toggle_anim)

        exporter = window.createAction("toggle_docker_exporter", "Toggle Exporter Docker")
        exporter.triggered.connect(self.toggle_exporter)

        grayscale = window.createAction("toggle_grayscale", "Toggle Grayscale")
        grayscale.triggered.connect(self.toggle_grayscale)

    def toggle_anim(self):
        self.toggle_docker("Animation Timeline")

    def toggle_exporter(self):
        self.toggle_docker("Exporter")

    def toggle_docker(self, name):
        d = Krita.instance().dockers()
        for x in d:
            if x.windowTitle() == name:
                x.setVisible(not x.isVisible())

    def toggle_grayscale(self):
        doc = Krita.instance().activeDocument()
        node = self._get_grayscale_node(doc)
        node.setVisible(not node.visible())
        doc.refreshProjection()

    def _get_grayscale_node(self, doc):
        last = None
        for node in doc.topLevelNodes():
            last = node
            if node.name() == grayscale_node:
                return node

        info = InfoObject()
        info.setProperty("color", "#FFFFFF")

        sel = Selection()
        sel.select(0, 0, doc.width(), doc.height(), 255)

        new_node = doc.createFillLayer(grayscale_node, "color", info, sel)
        doc.rootNode().addChildNode(new_node, last)
        new_node.setBlendingMode("color")
        new_node.setVisible(False) # It will be toggled immediately after
        return new_node

