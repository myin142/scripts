# Hide/Show all layers of a group
# Useful for the exporter, nodes need to be visible to be exported

doc = Krita.instance().activeDocument()
group = doc.activeNode()

while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

visible = not doc.activeNode().visible()
for child in group.childNodes():
    child.setVisible(visible)
doc.refreshProjection()
doc.waitForDone()
