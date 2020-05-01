import xml.etree.ElementTree as ET

def parseXML(filePath):
    tree = ET.parse(filePath)
    return tree

def printTree(tree):
    for elem in tree.getroot().iter():
        print(elem.tag, elem.text)