# MHTML to PDF Converter

This is a simple Python script to convert MHTML (`.mhtml` or `.mht`) files to PDF documents.

## Requirements

- Python 3.6+

## Installation

1. Clone this repository.
2. Install the required Python packages using pip:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

To convert an MHTML file to PDF, run the `mhtml_to_pdf.py` script from the command line:

```bash
python mhtml_to_pdf.py <input_mhtml_file> <output_pdf_file>
```

### Example

```bash
python mhtml_to_pdf.py sample.mhtml converted_document.pdf
```

This will create a new file named `converted_document.pdf` in the same directory.

## How it works

The script parses the MHTML file, which is a MIME-encoded archive, to extract the main HTML content and any embedded resources (like images and CSS). It then converts the `cid:` links for these resources into base64-encoded data URIs, so they can be embedded directly in the HTML. Finally, it uses the WeasyPrint library to render the HTML with the embedded resources into a PDF document.