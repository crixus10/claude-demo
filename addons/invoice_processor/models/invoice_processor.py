from odoo import models, fields, api
from odoo.exceptions import UserError
import anthropic
import base64
import logging

_logger = logging.getLogger(__name__)


class InvoiceProcessor(models.Model):
    _name = 'invoice.processor'
    _description = 'AI Invoice Processor'
    _rec_name = 'invoice_name'

    invoice_name = fields.Char('Invoice Name', required=True)
    pdf_file = fields.Binary('PDF File', required=True)
    pdf_filename = fields.Char('Filename')
    
    # Extracted Fields
    vendor_id = fields.Many2one('res.partner', 'Vendor')
    invoice_number = fields.Char('Invoice Number')
    invoice_date = fields.Date('Invoice Date')
    due_date = fields.Date('Due Date')
    amount = fields.Float('Amount')
    currency_id = fields.Many2one('res.currency', 'Currency')
    description = fields.Text('Description')
    
    # Status
    state = fields.Selection([
        ('draft', 'Draft'),
        ('processed', 'Processed'),
        ('error', 'Error'),
    ], default='draft')
    
    processing_log = fields.Text('Processing Log')
    created_bill_id = fields.Many2one('account.move', 'Created Bill')

    @api.model
    def _get_claude_client(self):
        """Initialize Anthropic client"""
        api_key = self.env['ir.config_parameter'].sudo().get_param(
            'invoice_processor.claude_api_key'
        )
        if not api_key:
            raise UserError('Claude API key not configured. Go to Settings > Invoice Processor.')
        return anthropic.Anthropic(api_key=api_key)

    def process_invoice(self):
        """Process PDF with Claude AI"""
        self.ensure_one()
        
        try:
            client = self._get_claude_client()
            pdf_b64 = base64.b64encode(self.pdf_file).decode('utf-8')
            
            prompt = """
            Extract the following information from this invoice PDF:
            - Vendor/Supplier name
            - Invoice number
            - Invoice date (format: YYYY-MM-DD)
            - Due date (format: YYYY-MM-DD)
            - Total amount
            - Currency
            - Line items description
            
            Return as JSON only, no extra text.
            """
            
            message = client.messages.create(
                model="claude-3-5-sonnet-20241022",
                max_tokens=1024,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "document",
                                "source": {
                                    "type": "base64",
                                    "media_type": "application/pdf",
                                    "data": pdf_b64,
                                },
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ],
                    }
                ],
            )
            
            response_text = message.content[0].text
            _logger.info(f"Claude response: {response_text}")
            
            # Parse response and update fields
            import json
            try:
                data = json.loads(response_text)
                self._update_from_claude_response(data)
                self.state = 'processed'
                self.processing_log = f"Successfully processed with Claude AI\n{response_text}"
            except json.JSONDecodeError:
                self.state = 'error'
                self.processing_log = f"Failed to parse Claude response:\n{response_text}"
                
        except Exception as e:
            self.state = 'error'
            self.processing_log = f"Error: {str(e)}"
            _logger.error(f"Invoice processing error: {str(e)}")

    def _update_from_claude_response(self, data):
        """Update model fields from Claude response"""
        # Find or create vendor
        vendor_name = data.get('vendor_name') or data.get('supplier_name')
        if vendor_name:
            vendor = self.env['res.partner'].search([
                ('name', 'ilike', vendor_name)
            ], limit=1)
            if not vendor:
                vendor = self.env['res.partner'].create({
                    'name': vendor_name,
                    'is_company': True,
                })
            self.vendor_id = vendor.id

        self.invoice_number = data.get('invoice_number', '')
        self.invoice_date = data.get('invoice_date')
        self.due_date = data.get('due_date')
        self.amount = data.get('amount', 0.0)
        
        currency_code = data.get('currency', 'EUR')
        currency = self.env['res.currency'].search([
            ('name', '=', currency_code)
        ], limit=1)
        if currency:
            self.currency_id = currency.id

        self.description = data.get('description', '')

    def create_bill(self):
        """Create bill in Odoo from processed invoice"""
        self.ensure_one()
        
        if self.state != 'processed':
            raise UserError('Invoice must be processed first.')
        
        if not self.vendor_id:
            raise UserError('Vendor not found. Please process the invoice first.')

        bill_lines = []
        bill_lines.append((0, 0, {
            'name': self.description or f"Invoice {self.invoice_number}",
            'quantity': 1.0,
            'price_unit': self.amount,
            'account_id': self.env['account.account'].search([
                ('account_type', '=', 'expense')
            ], limit=1).id,
        }))

        bill = self.env['account.move'].create({
            'move_type': 'in_invoice',
            'partner_id': self.vendor_id.id,
            'invoice_date': self.invoice_date,
            'ref': self.invoice_number,
            'line_ids': bill_lines,
            'currency_id': self.currency_id.id,
        })

        self.created_bill_id = bill.id
        self.processing_log += f"\nBill created: {bill.name}"
