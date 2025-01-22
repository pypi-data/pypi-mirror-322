from lxml import etree
import re
import os

def clean_xml_from_file(filepath, output_filepath, encoding='utf-8', remove_namespaces=True):
    """
    Clean XML file and save to new file.
    
    Args:
        filepath (str): Path to input XML file
        output_filepath (str): Path to save cleaned XML
        encoding (str): File encoding
        remove_namespaces (bool): Whether to remove XML namespaces
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        with open(filepath, 'r', encoding=encoding) as f:
            xml_string = f.read()
        cleaned_xml = clean_xml(xml_string, encoding=encoding, remove_namespaces=remove_namespaces)
        if cleaned_xml:
            os.makedirs(os.path.dirname(output_filepath), exist_ok=True)
            with open(output_filepath, 'w', encoding=encoding) as outfile:
                outfile.write(cleaned_xml)
            return True
        else:
            return False
    except FileNotFoundError:
        print(f"Error: File not found at {filepath}")
        return False
    except Exception as e:
        print(f"An error occurred: {e}")
        return False

def clean_xml(xml_string, encoding='utf-8', remove_namespaces=True):
    """
    Clean XML string.
    
    Args:
        xml_string (str): XML content to clean
        encoding (str): XML encoding
        remove_namespaces (bool): Whether to remove XML namespaces
        
    Returns:
        str: Cleaned XML string
    """
    xml_string = re.sub(r'<\?xml[^>]*\?>', '', xml_string)
    try:
        if isinstance(xml_string, str):
            xml_string = xml_string.encode(encoding)
        parser = etree.XMLParser(remove_blank_text=True, recover=True)
        tree = etree.fromstring(xml_string, parser=parser)
    except etree.XMLSyntaxError as e:
        print(f"XML Syntax Error: {e}")
        return None  

    if remove_namespaces:
        for el in tree.iter():
            if el.tag and '}' in el.tag:
                el.tag = el.tag.split('}', 1)[1]
            for attrib_name in list(el.attrib):
                if '}' in attrib_name:
                    del el.attrib[attrib_name]

    def normalize_whitespace(element):
        if element.text:
            element.text = " ".join(element.text.split())  
        if element.tail:
           element.tail = " ".join(element.tail.split()) 
        for child in element:
            normalize_whitespace(child)
    normalize_whitespace(tree)

    def remove_trailing_spaces(element):
        if element.text:
            element.text = element.text.strip()
        if element.tail:
            element.tail = element.tail.strip()
        for child in element:
            remove_trailing_spaces(child)
    remove_trailing_spaces(tree)

    def remove_empty_tags(element):
        for child in list(element):
            remove_empty_tags(child)
            if not child.text and not child.attrib and not len(child):
                element.remove(child)
    remove_empty_tags(tree)

    cleaned_xml = etree.tostring(tree, encoding=encoding, pretty_print=True, xml_declaration=True).decode(encoding)
    return cleaned_xml