{
    'name': 'Niubiz Payment Provider',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Payment Provider: Niubiz Peru',
    'description': """
    Integración con Niubiz Perú para procesar pagos con tarjetas.
    Soporte para tarjetas de crédito y débito Visa y Mastercard.
    """,
    'depends': ['payment'],
    'data': [
        'views/payment_niubiz_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_method_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}