# -*- coding: utf-8 -*-
{
    'name': 'Flywire Payment Gateway',
    'version': '1.0.0',
    'summary': 'Integración con pasarela de pago Flywire',
    'author': 'Breithner Aquituari',
    'category': 'Accounting/Payment Acquirers',
    'depends': ['payment', 'website_sale'],
    'data': [
        'views/payment_flywire_templates.xml',
        'data/payment_method_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}