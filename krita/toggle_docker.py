#w = Krita.resources('workspace')['Animation']
#x = [method_name for method_name in dir(w) if callable(getattr(w, method_name))]
#print(x)


#object_methods = [method_name for method_name in dir(mw) if callable(getattr(mw, method_name))]
#print(object_methods)

#mw = Krita.activeWindow().qwindow()
#mw.restoreWorkspaceState()

d = Krita.dockers()

for x in d:
    if x.windowTitle() == "Animation Timeline":
        x.setVisible(not x.isVisible())