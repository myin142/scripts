# Collapses or expands all layers in the active group

doc = Krita.instance().activeDocument()
group = doc.activeNode()

while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

collapsed = doc.activeNode().collapsed()
for child in group.childNodes():
    child.setCollapsed(not collapsed)
doc.refreshProjection()
doc.waitForDone()