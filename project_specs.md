# Project Spec: Invoice Processing System

## Goal
Automatically process PDF invoices from the `/PDFs` folder:
1. Extract structured data using Claude AI
2. Rename files to `[Provider] - [YYYY-MM-DD].pdf`
3. Organise into monthly subfolders (`PDFs/YYYY-MM - Month Name/`)
4. Export all data to `invoices_YYYY.csv`

---

## Input
- PDF invoice files placed in `/PDFs/` (top-level)
- Files may have any name

## Output
- Renamed PDFs moved into month subfolders under `/PDFs/`
- A CSV file at the project root: `invoices_YYYY.csv`

## CSV Schema
| Field | Description |
|---|---|
| filename | Final renamed filename |
| provider | Business/vendor name |
| invoice_date | YYYY-MM-DD |
| due_date | YYYY-MM-DD (if present) |
| invoice_number | Invoice reference number |
| line_items | Semicolon-separated: `Description x Qty @ Rate` |
| subtotal | Numeric |
| tax | Numeric |
| total | Numeric |

---

## Tech Stack
- Python 3
- Claude API (`claude-sonnet-4-6`) for invoice data extraction
- `pdfplumber` for text extraction
- `PyMuPDF` for page-to-image rendering
- `python-dotenv` for env management

## Entry Point
```
python src/main.py
```

## Environment Variables
- `ANTHROPIC_API_KEY` — required

---

## Constraints
- Do not modify PDFs that are already in month subfolders
- Never commit `.env`
- One CSV per year, appended if re-run
