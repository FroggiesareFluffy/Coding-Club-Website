import xml.etree.ElementTree as ETree
import sys

class XMLObject(object):
    def __init__(self,text,tail,**options):
        self.children = []
        self.text = text
        self.tail = tail
        for name,value in options.items():
            setattr(self,name,value)

def load_xml(xml_file_name,potential_types):
    tree = ETree.parse(xml_file_name)
    root = tree.getroot()
    new_root = convert_obj(root,potential_types)
    return new_root

def convert_obj(element,potential_types):
    class_name = element.tag
    attributes = element.attrib
    text = element.text
    tail = element.tail
    obj = potential_types[class_name](text,tail,**attributes)
    for o in element:
        obj.children.append(convert_obj(o,potential_types))
    return obj
