# Hide/Show all layers of a group
# Useful for the exporter, nodes need to be visible to be exported

doc = Krita.instance().activeDocument()
group = doc.activeNode()

while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

for child in group.childNodes():
    child.setVisible(not child.visible())
doc.refreshProjection()
doc.waitForDone()