from .downloader import download_xml_file
from .cleaner import clean_xml_from_file
from .xslt_generator import generate_dynamic_xslt
from .converter import transform_xml_to_pdf

class XMLToPDFConverter:
    def __init__(self, download_dir='downloads'):
        self.download_dir = download_dir
        
    def url_to_pdf(self, url, output_pdf):
        """Convert XML from URL to PDF"""
        # Download
        xml_file = download_xml_file(url, self.download_dir)
        if not xml_file:
            raise Exception("Failed to download XML file")
            
        return self.file_to_pdf(xml_file, output_pdf)
        
    def file_to_pdf(self, input_xml, output_pdf):
        """Convert local XML file to PDF"""
        import os
        
        # Clean XML
        cleaned_xml = f"{os.path.splitext(input_xml)[0]}_cleaned.xml"
        if not clean_xml_from_file(input_xml, cleaned_xml):
            raise Exception("Failed to clean XML")
            
        # Generate XSLT
        xslt_file = f"{os.path.splitext(input_xml)[0]}.xslt"
        generate_dynamic_xslt(cleaned_xml, xslt_file)
        
        # Convert to PDF
        transform_xml_to_pdf(cleaned_xml, xslt_file, output_pdf)
        return output_pdf

__all__ = ['XMLToPDFConverter']