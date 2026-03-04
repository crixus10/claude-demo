# Invoice Processor AI — Odoo 19 Module

AI-powered invoice processing for Odoo 19 using Claude API.

## Features

- 📄 Upload PDF invoices
- 🤖 Automatic extraction using Claude AI
- 💾 Save extracted data to Odoo
- 📝 Create bills automatically
- 📊 Track processing status

## Installation

1. Clone or copy this module to `addons/` folder
2. Restart Odoo server
3. Install module: Apps → Search "Invoice Processor" → Install
4. Configure Claude API key in Settings

## Configuration

1. Go to Settings → Technical → System Parameters
2. Create new parameter:
   - Key: `invoice_processor.claude_api_key`
   - Value: Your Claude API key from Anthropic

## Usage

1. Go to Invoice Processor → Invoices
2. Create new invoice
3. Upload PDF file
4. Click "Process with Claude"
5. Verify extracted data
6. Click "Create Bill" to generate bill in Odoo

## Requirements

```
anthropic>=0.7.0
PyPDF2>=3.0.0
```

## Dependencies

- base
- account
- purchase

## Author

Sorin Trifu @ Mittani Solutions

## License

LGPL-3
