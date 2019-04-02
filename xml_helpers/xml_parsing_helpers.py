#!/usr/bin/env python3
"""
    Purpose:
        Library for parsing XML objects in Python
"""

# Python Library Imports
import logging
import xml.etree.ElementTree as ET


def convert_xml_tree_to_dict(root_element):
    """
    Purpose:
        Parse an XML Tree (the root element should be passed in)
        recursivly into a python Dict. This will use key/value pairs
        where the key is the node tag and the values is the text. Ignores
        attrbs of the tags for now
    Args:
        root_element (Element of ET Class): XML Root Node to Traverse
    Returns:
        xml_dict (Dicts): Dict resulting from parsed XML
    """

    xml_dict = {}
    for element in root_element:
        if element.text:
            xml_dict[element.tag] = element.text
        else:
            xml_dict[element.tag] = convert_xml_tree_to_dict(element)

    return xml_dict
