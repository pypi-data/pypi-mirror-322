# XML2PDF Converter

A Python library to convert XML files to PDF format.

## Installation

```bash
pip install xml2pdf
```

## Dependencies
- Python 3.6+
- requests
- lxml
- weasyprint

## Usage

```python
from xml2pdf import XMLToPDFConverter

# Initialize the converter
converter = XMLToPDFConverter()

# Convert XML from URL to PDF
converter.url_to_pdf("https://example.com/file.xml", "output.pdf")

# Or convert local XML file to PDF
converter.file_to_pdf("input.xml", "output.pdf")
```

## Features
- Download XML files from URLs
- Clean and normalize XML content
- Generate dynamic XSLT templates
- Convert XML to PDF with customizable styling

## License
MIT License

## Author
- Hirthickkesh
- Email: hirthickkeshpr@gmail.com
- GitHub: https://github.com/Higgy-debug