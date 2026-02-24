"""
file_organizer.py
Renames invoice PDFs and moves them into month subfolders.
"""

import shutil
import re
from pathlib import Path
from datetime import datetime


MONTH_NAMES = {
    1: "January", 2: "February", 3: "March", 4: "April",
    5: "May", 6: "June", 7: "July", 8: "August",
    9: "September", 10: "October", 11: "November", 12: "December",
}


def _safe_name(value: str) -> str:
    """Remove characters that are unsafe in filenames."""
    return re.sub(r'[<>:"/\\|?*]', "", value).strip()


def organise_invoice(pdf_path: Path, provider: str, invoice_date: str, pdfs_root: Path) -> Path:
    """
    Rename the PDF to '[Provider] - [YYYY-MM-DD].pdf' and move it into
    'pdfs_root/YYYY-MM - Month Name/'. Returns the new path.

    If a file with the target name already exists, a numeric suffix is appended.
    """
    safe_provider = _safe_name(provider)
    new_name = f"{safe_provider} - {invoice_date}.pdf"

    # Determine month folder
    date_obj = datetime.strptime(invoice_date, "%Y-%m-%d")
    month_folder_name = f"{date_obj.year}-{date_obj.month:02d} - {MONTH_NAMES[date_obj.month]}"
    month_folder = pdfs_root / month_folder_name
    month_folder.mkdir(parents=True, exist_ok=True)

    target = month_folder / new_name

    # Avoid overwriting an existing file
    if target.exists() and target != pdf_path:
        stem = f"{safe_provider} - {invoice_date}"
        counter = 1
        while target.exists():
            target = month_folder / f"{stem} ({counter}).pdf"
            counter += 1

    shutil.move(str(pdf_path), str(target))
    return target
