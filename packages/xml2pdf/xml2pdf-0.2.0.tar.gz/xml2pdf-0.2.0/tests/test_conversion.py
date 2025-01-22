import os
from xml2pdf import (
    download_xml_file,
    clean_xml_from_file,
    generate_dynamic_xslt,
    transform_xml_to_pdf
)

def test_full_conversion():
    # URL of your XML file
    url = "https://mtnewswires3.com/editpad/view_press.php?f=202501160200RNS_____UKDISCLO_20250116_5070T.xml"
    
    # Create output directory
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        # Step 1: Download XML
        print("1. Downloading XML file...")
        xml_file = download_xml_file(url, save_dir=output_dir)
        if not xml_file:
            print("Failed to download XML file")
            return
        print(f"✅ XML downloaded: {xml_file}")
        
        # Step 2: Clean XML
        print("\n2. Cleaning XML file...")
        cleaned_file = os.path.join(output_dir, f"cleaned_{os.path.basename(xml_file)}")
        if not clean_xml_from_file(xml_file, cleaned_file):
            print("Failed to clean XML file")
            return
        print(f"✅ XML cleaned: {cleaned_file}")
        
        # Step 3: Generate XSLT
        print("\n3. Generating XSLT...")
        xslt_file = os.path.join(output_dir, "template.xslt")
        generate_dynamic_xslt(cleaned_file, xslt_file)
        print(f"✅ XSLT generated: {xslt_file}")
        
        # Step 4: Convert to PDF
        print("\n4. Converting to PDF...")
        pdf_file = os.path.join(output_dir, "final_output.pdf")
        transform_xml_to_pdf(cleaned_file, xslt_file, pdf_file)
        print(f"✅ PDF generated: {pdf_file}")
        
        print("\n🎉 Conversion completed successfully!")
        print("\nOutput files:")
        print(f"- Original XML: {xml_file}")
        print(f"- Cleaned XML: {cleaned_file}")
        print(f"- XSLT file: {xslt_file}")
        print(f"- PDF file: {pdf_file}")
        
    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

if __name__ == "__main__":
    test_full_conversion()