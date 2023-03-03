doc = Krita.instance().activeDocument()
mask = doc.activeNode()



if not mask.type().endswith('mask'):
    print("Node is not a mask: " + mask.type())
else:
    parent = mask.parentNode()

    def flatten_with_mask(node, mask):
        if node.childNodes():
            for child in node.childNodes():
                flatten_with_mask(child, mask)
        else:
            print("Apply and flatten: %s" % node.name())
            node.addChildNode(mask.clone(), None)
            doc.setActiveNode(node)
            Krita.action('flatten_layer').trigger()
            doc.waitForDone()

    if parent and parent.childNodes():
        for child in parent.childNodes():
            if child == mask: continue
            flatten_with_mask(child, mask)
        