{
    'name': 'Culqi Payment Provider',
    'version': '19.0.1.0.0',
    'category': 'Accounting/Payment Providers',
    'summary': 'Payment Provider: Culqi Peru',
    'description': """
    Integración con Culqi Perú para procesar pagos con tarjetas.
    Soporte para tarjetas de crédito, débito y billeteras digitales.
    """,
    'depends': ['payment'],
    'data': [
        'views/payment_culqi_templates.xml',
        'views/payment_provider_views.xml',
        'data/payment_method_data.xml',
    ],
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}