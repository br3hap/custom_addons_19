# -*- coding: utf-8 -*-
{
    'name': 'Mi Módulo OWL',
    'version': '1.0.0',
    'summary': """ Mi_modulo_owl Summary """,
    'author': 'Breithner Aquituari',
    'category': 'Tools',
    'depends': ['base', 'web', 'website', 'sale'],
    'data': [
        'views/menu_accion.xml',
        'views/usuarios_template.xml',
    ],
    'assets': {
        'web.assets_backend': [
            'mi_modulo_owl/static/src/components.js',
            'mi_modulo_owl/static/src/templates.xml',
        ],
        'web.assets_frontend': [
            'mi_modulo_owl/static/src/components.js',
        ],
    },
    
    'application': True,
    'installable': True,
    'auto_install': False,
    'license': 'LGPL-3',
}
