from lxml import etree
from weasyprint import HTML

def transform_xml_to_pdf(xml_file, xslt_file, pdf_file):
    try:
        xml_tree = etree.parse(xml_file)
        xslt_tree = etree.parse(xslt_file)

        transform = etree.XSLT(xslt_tree)
        transformed_xml = transform(xml_tree)

        html_text = str(transformed_xml)

        HTML(string=html_text).write_pdf(pdf_file)

        print(f"PDF generated successfully: {pdf_file}")

    except etree.XMLSyntaxError as e:
        print(f"Error: XML syntax error while processing: {e}")

    except etree.XSLTParseError as e:
         print(f"Error: XSLT Parse error while processing: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")