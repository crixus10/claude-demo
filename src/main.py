"""
main.py
Orchestrates the invoice processing pipeline:
  1. Scan /PDFs for top-level PDF files
  2. Extract text + image from each PDF
  3. Parse invoice data via Claude API
  4. Rename and move files into month folders
  5. Append records to invoices_YYYY.csv
"""

import os
import sys
from pathlib import Path

import anthropic
from dotenv import load_dotenv

from pdf_reader import extract_text, render_first_page_as_base64
from invoice_parser import parse_invoice
from file_organizer import organise_invoice
from csv_exporter import append_record

load_dotenv()

PDFS_ROOT = Path(__file__).parent.parent / "PDFs"
PROJECT_ROOT = Path(__file__).parent.parent


def get_csv_path(invoice_date: str) -> Path:
    year = invoice_date[:4] if invoice_date else "unknown"
    return PROJECT_ROOT / f"invoices_{year}.csv"


def process_pdf(pdf_path: Path, client: anthropic.Anthropic) -> None:
    print(f"Processing: {pdf_path.name}")

    text = extract_text(str(pdf_path))
    image_b64 = render_first_page_as_base64(str(pdf_path))

    data = parse_invoice(text, image_b64, client)

    provider = data.get("provider") or "Unknown Provider"
    invoice_date = data.get("invoice_date") or "1900-01-01"

    new_path = organise_invoice(pdf_path, provider, invoice_date, PDFS_ROOT)
    print(f"  -> Moved to: {new_path.relative_to(PROJECT_ROOT)}")

    csv_path = get_csv_path(invoice_date)
    append_record(csv_path, new_path.name, data)
    print(f"  -> Recorded in: {csv_path.name}")


def main():
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set in environment / .env file.")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=api_key)

    # Only process PDFs at the top level (not already-organised subfolders)
    pdf_files = [p for p in PDFS_ROOT.iterdir() if p.is_file() and p.suffix.lower() == ".pdf"]

    if not pdf_files:
        print("No PDF files found in the PDFs folder.")
        return

    print(f"Found {len(pdf_files)} PDF(s) to process.\n")
    errors = []

    for pdf_path in pdf_files:
        try:
            process_pdf(pdf_path, client)
        except Exception as e:
            print(f"  ERROR processing {pdf_path.name}: {e}")
            errors.append((pdf_path.name, str(e)))

    print(f"\nDone. {len(pdf_files) - len(errors)} succeeded, {len(errors)} failed.")
    if errors:
        for name, err in errors:
            print(f"  - {name}: {err}")


if __name__ == "__main__":
    main()
