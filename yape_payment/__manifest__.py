{
    'name': 'Yape Payment Provider',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Payment Provider: Yape Peru',
    'description': """
    Integración con Yape Perú para procesar pagos móviles.
    Soporte para QR y transferencias instantáneas.
    """,
    'depends': ['payment'],
    'data': [
        'views/payment_yape_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_method_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}