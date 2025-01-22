# XML2PDF Converter

A Python library to convert XML files to PDF format. This tool can download XML files from URLs, clean them, and convert them to well-formatted PDFs.

## Features

- Download XML files from URLs
- Clean and normalize XML content
- Generate dynamic XSLT templates
- Convert XML to PDF with customizable styling
- Support for both local files and URLs

## Installation

### Using pip

```bash
pip install xml2pdf
```

### Using conda environment

```bash
# First install dependencies
conda install requests lxml weasyprint

# Then install xml2pdf
pip install xml2pdf
```

## Usage

### Converting XML from URL

```python
from xml2pdf import XMLToPDFConverter

# Initialize the converter
converter = XMLToPDFConverter()

# Convert XML from URL to PDF
url = "https://example.com/file.xml"
output_pdf = "output.pdf"
converter.url_to_pdf(url, output_pdf)
```

### Converting Local XML File

```python
from xml2pdf import XMLToPDFConverter

converter = XMLToPDFConverter()

# Convert local XML file to PDF
input_xml = "input.xml"
output_pdf = "output.pdf"
converter.file_to_pdf(input_xml, output_pdf)
```

## Dependencies

- Python 3.6+
- requests
- lxml
- weasyprint

## Error Handling

The library includes comprehensive error handling for:
- Network issues during XML download
- XML parsing errors
- File system operations
- PDF generation issues

## Contributing

Feel free to open issues or submit pull requests on GitHub.

## License

MIT License

## Author

- Hirthickkesh
- Email: hirthickkeshpr@gmail.com
- GitHub: https://github.com/Higgy-debug