doc = Krita.instance().activeDocument()
group = doc.activeNode()
while group and not group.type().startswith('group'):
    group = group.parentNode()

if not group:
    print("No group found")
    exit()

children = group.childNodes()
length = len(children)
for i in range(length):
    children[i].setName(f"{i}")