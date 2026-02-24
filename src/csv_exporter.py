"""
csv_exporter.py
Writes invoice records to a yearly CSV file.
"""

import csv
from pathlib import Path

FIELDNAMES = [
    "filename",
    "provider",
    "invoice_date",
    "due_date",
    "invoice_number",
    "line_items",
    "subtotal",
    "tax",
    "total",
]


def _format_line_items(line_items: list) -> str:
    parts = []
    for item in line_items:
        desc = item.get("description", "")
        qty = item.get("quantity", "")
        rate = item.get("rate", "")
        subtotal = item.get("subtotal", "")
        parts.append(f"{desc} x{qty} @ {rate} = {subtotal}")
    return "; ".join(parts)


def append_record(csv_path: Path, filename: str, data: dict) -> None:
    """Append a single invoice record to the CSV. Creates the file with headers if new."""
    write_header = not csv_path.exists()

    with csv_path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDNAMES)
        if write_header:
            writer.writeheader()

        writer.writerow({
            "filename": filename,
            "provider": data.get("provider", ""),
            "invoice_date": data.get("invoice_date", ""),
            "due_date": data.get("due_date", ""),
            "invoice_number": data.get("invoice_number", ""),
            "line_items": _format_line_items(data.get("line_items", [])),
            "subtotal": data.get("subtotal", ""),
            "tax": data.get("tax", ""),
            "total": data.get("total", ""),
        })
