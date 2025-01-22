from lxml import etree
from weasyprint import HTML

def transform_xml_to_pdf(xml_file, xslt_file, pdf_file):
    """
    Transform XML to PDF using XSLT and WeasyPrint.
    
    Args:
        xml_file (str): Path to input XML file
        xslt_file (str): Path to XSLT file
        pdf_file (str): Path to save output PDF
    """
    try:
        # Load XML and XSLT
        xml_tree = etree.parse(xml_file)
        xslt_tree = etree.parse(xslt_file)

        # Perform XSLT Transformation
        transform = etree.XSLT(xslt_tree)
        transformed_xml = transform(xml_tree)

        # Convert to HTML text
        html_text = str(transformed_xml)

        # Generate PDF
        HTML(string=html_text).write_pdf(pdf_file)
        
        print(f"PDF generated successfully: {pdf_file}")
    
    except etree.XMLSyntaxError as e:
        print(f"Error: XML syntax error while processing: {e}")
    except etree.XSLTParseError as e:
        print(f"Error: XSLT Parse error while processing: {e}")
    except Exception as e:
        print(f"An error occurred: {e}")