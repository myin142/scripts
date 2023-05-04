from krita import Extension
#w = Krita.resources('workspace')['Animation']
#x = [method_name for method_name in dir(w) if callable(getattr(w, method_name))]
#print(x)


#object_methods = [method_name for method_name in dir(mw) if callable(getattr(mw, method_name))]
#print(object_methods)

#mw = Krita.activeWindow().qwindow()
#mw.restoreWorkspaceState()


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

    def toggle_anim(self):
        self.toggle_docker("Animation Timeline")

    def toggle_exporter(self):
        self.toggle_docker("Exporter")

    def toggle_docker(self, name):
        d = Krita.dockers()
        for x in d:
            if x.windowTitle() == name:
                x.setVisible(not x.isVisible())

