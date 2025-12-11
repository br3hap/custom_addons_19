# -*- coding: utf-8 -*-
{
    'name': 'Componente Publico',
    'version': '1.0.0',
    'summary': """ Componente Publico """,
    'author': 'Breithner Aquituari',
    'website': '',
    'category': '',
    'depends': ['base', ],
    'data': [
        'views/website_template.xml',
    ],
    'assets': {
        'web.assets_frontend_lazy': [
            'component_public/static/src/components/partner_simple_component/partner_simple_component.xml',
            'component_public/static/src/components/partner_simple_component/partner_simple_component.js',
        ],
    },
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
