#!/usr/bin/python

from lxml import etree as et

filename = 'Devices_2016-06-01_00-23-55.csv'
xml_filename = "cameras.xml"

root = et.Element("cameras")

f = open(filename, "r")
i = 0
for line in f:
    if i <> 0:
        items = line.split(";")
        camera = et.Element('cam', {"configured":"0"})
        camera.attrib["ipAddress"] = items[2]
        camera.attrib["model"] = items[4].split()[1]
        camera.attrib["macAddress"] = items[0]
        root.append(camera)
    i += 1
f.close()
f = open(xml_filename, "w")
f.write(et.tostring(root, pretty_print=True, xml_declaration=True, encoding='utf-8'))
f.close()