# tests/test_conversion.py
import os
import sys
from pathlib import Path

# Get the absolute path to the project root
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
src_path = os.path.join(project_root, 'src')

# Add to Python path
sys.path.insert(0, src_path)

# Now import the modules
from xm2pdf.downloader import download_xml_file
from xm2pdf.cleaner import clean_xml_from_file
from xm2pdf.xslt_generator import generate_dynamic_xslt
from xm2pdf.converter import transform_xml_to_pdf

def test_full_conversion():
    # URL of your XML file
    url = "https://mtnewswires3.com/editpad/view_press.php?f=202501160200RNS_____UKDISCLO_20250116_5070T.xml"
    
    # Create output directories
    os.makedirs("output", exist_ok=True)
    
    try:
        # Step 1: Download XML
        print("Downloading XML file...")
        xml_file = download_xml_file(url, save_dir="output")
        if not xml_file:
            print("Failed to download XML file")
            return
        
        # Step 2: Clean XML
        print("Cleaning XML file...")
        cleaned_file = os.path.join("output", "cleaned_" + os.path.basename(xml_file))
        if not clean_xml_from_file(xml_file, cleaned_file):
            print("Failed to clean XML file")
            return
        
        # Step 3: Generate XSLT
        print("Generating XSLT...")
        xslt_file = os.path.join("output", "template.xslt")
        generate_dynamic_xslt(cleaned_file, xslt_file)
        
        # Step 4: Convert to PDF
        print("Converting to PDF...")
        pdf_file = os.path.join("output", "final_output.pdf")
        transform_xml_to_pdf(cleaned_file, xslt_file, pdf_file)
        
        print("\nConversion completed successfully!")
        print(f"Output files in the 'output' directory:")
        print(f"- Original XML: {xml_file}")
        print(f"- Cleaned XML: {cleaned_file}")
        print(f"- XSLT file: {xslt_file}")
        print(f"- PDF file: {pdf_file}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_full_conversion()