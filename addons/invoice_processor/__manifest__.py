{
    'name': 'Invoice Processor AI',
    'version': '19.0.1.0.0',
    'category': 'Accounting',
    'summary': 'AI-powered invoice processing with Claude API',
    'author': 'Sorin Trifu',
    'license': 'LGPL-3',
    'depends': [
        'base',
        'account',
        'purchase',
    ],
    'data': [
        'views/invoice_processor_views.xml',
        'views/menu.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
        'python': [
            'anthropic',
            'PyPDF2',
        ],
    },
    'installable': True,
    'application': True,
    'auto_install': False,
}
