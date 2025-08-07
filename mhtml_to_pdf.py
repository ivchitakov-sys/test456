import argparse
import base64
from email import message_from_bytes
from email.policy import default
import mimetypes
from pathlib import Path
from urllib.parse import unquote

from weasyprint import HTML

def convert_mhtml_to_pdf(mhtml_path: Path, pdf_path: Path):
    """
    Converts an MHTML file to a PDF file.
    """
    with open(mhtml_path, "rb") as f:
        mhtml_content = f.read()

    msg = message_from_bytes(mhtml_content, policy=default)

    html_part = None
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html_part = part
            break

    if not html_part:
        raise ValueError("MHTML file does not contain an HTML part.")

    resources = {}
    for part in msg.walk():
        if part.get_content_maintype() == "multipart":
            continue
        if part.get("Content-ID"):
            cid = part.get("Content-ID").strip("<>")
            content_type = part.get_content_type()
            data = part.get_payload(decode=True)
            resources[cid] = (content_type, data)

    charset = html_part.get_content_charset() or "utf-8"
    html_content = html_part.get_payload(decode=True).decode(charset)

    for cid, (content_type, data) in resources.items():
        b64_data = base64.b64encode(data).decode("utf-8")
        data_uri = f"data:{content_type};base64,{b64_data}"
        html_content = html_content.replace(f"cid:{cid}", data_uri)

    HTML(string=html_content).write_pdf(pdf_path)

def main():
    """
    Main function to handle command-line arguments.
    """
    parser = argparse.ArgumentParser(description="Convert an MHTML document to a PDF.")
    parser.add_argument("mhtml_path", type=Path, help="Path to the input MHTML file.")
    parser.add_argument("pdf_path", type=Path, help="Path to the output PDF file.")
    args = parser.parse_args()

    convert_mhtml_to_pdf(args.mhtml_path, args.pdf_path)

if __name__ == "__main__":
    main()
