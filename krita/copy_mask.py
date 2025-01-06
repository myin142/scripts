# Copy mask to all sibling layers

doc = Krita.instance().activeDocument()
mask = doc.activeNode()
if not mask.type().endswith('mask'):
    print("Node is not a mask: " + mask.type())
    exit()

group = doc.activeNode()
while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

for child in group.childNodes():
    if child == mask.parentNode(): continue
    child.addChildNode(mask.clone(), None)

doc.refreshProjection()
doc.waitForDone()