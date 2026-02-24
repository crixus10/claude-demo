"""
invoice_parser.py
Uses the Claude API to extract structured invoice data from PDF text and image.
"""

import json
from typing import Optional
import anthropic

SYSTEM_PROMPT = """You are an invoice data extraction assistant.
Given the text and/or image of an invoice, extract the following fields as JSON.
Return ONLY valid JSON, no explanation.

Fields:
- provider: string (the vendor/business issuing the invoice)
- invoice_date: string (YYYY-MM-DD format, or null if not found)
- due_date: string (YYYY-MM-DD format, or null if not found)
- invoice_number: string (or null)
- line_items: list of objects, each with keys: description, quantity, rate, subtotal
- subtotal: number (or null)
- tax: number (or null)
- total: number (or null)

Example output:
{
  "provider": "ACME Corp",
  "invoice_date": "2024-03-15",
  "due_date": "2024-04-15",
  "invoice_number": "INV-1001",
  "line_items": [
    {"description": "Web Design", "quantity": 1.0, "rate": 85.00, "subtotal": 85.00}
  ],
  "subtotal": 85.00,
  "tax": 8.50,
  "total": 93.50
}
"""


def parse_invoice(text: str, image_base64: Optional[str], client: anthropic.Anthropic) -> dict:
    """Send invoice content to Claude and return extracted data as a dict."""
    content = []

    if image_base64:
        content.append({
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": "image/png",
                "data": image_base64,
            },
        })

    user_text = "Extract all invoice data from this document."
    if text:
        user_text += f"\n\nExtracted text:\n{text}"

    content.append({"type": "text", "text": user_text})

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": content}],
    )

    raw = response.content[0].text.strip()
    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
    return json.loads(raw)
