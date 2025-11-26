# Hide/Show all layers of a group
# Useful for the exporter, nodes need to be visible to be exported

doc = Krita.instance().activeDocument()
group = doc.activeNode()

while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

print(f"Toggling {group.name()}")
visible = None

for child in group.childNodes():
    if visible == None:
        visible = not child.visible()
    child.setVisible(visible)
doc.refreshProjection()
doc.waitForDone()
