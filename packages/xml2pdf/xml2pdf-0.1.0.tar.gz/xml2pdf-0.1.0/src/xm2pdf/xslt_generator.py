import xml.etree.ElementTree as ET

def generate_dynamic_xslt(xml_file, xslt_file):
    """
    Generate XSLT file from XML structure.
    
    Args:
        xml_file (str): Path to input XML file
        xslt_file (str): Path to save generated XSLT
    """
    try:
        tree = ET.parse(xml_file)
        root = tree.getroot()
    except FileNotFoundError:
        print(f"Error: XML file not found at '{xml_file}'")
        return
    except ET.ParseError:
        print(f"Error: Could not parse XML file at '{xml_file}'")
        return

    xslt_root = ET.Element("xsl:stylesheet",
                        attrib={
                             "version": "1.0",
                             "xmlns": "http://www.w3.org/1999/xhtml",
                             "xmlns:xsl": "http://www.w3.org/1999/XSL/Transform"
                        },
                         nsmap={"xsl": "http://www.w3.org/1999/XSL/Transform"})

    # Root Template
    xslt_root_template = ET.SubElement(xslt_root, "xsl:template", match="/")
    xslt_root_apply_templates = ET.SubElement(xslt_root_template, "xsl:apply-templates")

    # General template for elements
    xslt_element_template = ET.SubElement(xslt_root, "xsl:template", match="*")
    xslt_element_copy = ET.SubElement(xslt_element_template, "xsl:element", name="{name()}")

    # Copy Attributes
    xslt_for_each = ET.SubElement(xslt_element_copy, "xsl:for-each", select="@*")
    xslt_attribute = ET.SubElement(xslt_for_each, "xsl:attribute", name="{name()}")
    xslt_value_of = ET.SubElement(xslt_attribute, "xsl:value-of", select=".")

    # Apply template for nested content
    xslt_apply_templates = ET.SubElement(xslt_element_copy, "xsl:apply-templates")

    # Template for text content
    xslt_text_template = ET.SubElement(xslt_root, "xsl:template", match="text()")
    xslt_text_value_of = ET.SubElement(xslt_text_template, "xsl:value-of", select=".")

    # Write to file
    xml_string = ET.tostring(xslt_root, encoding='utf-8', method='xml').decode()
    with open(xslt_file, 'w', encoding='utf-8') as f:
        f.write(xml_string)

    print(f"Dynamic XSLT file generated: '{xslt_file}'")