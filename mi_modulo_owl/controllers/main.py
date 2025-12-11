# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request

class UsuariosController(http.Controller):
    
    @http.route('/usuarios/lista', type='http', auth='user', website=True)
    def lista_usuarios(self):
        usuarios = request.env['res.users'].search([('active', '=', True)])
        return request.render('mi_modulo_owl.lista_usuarios_template', {
            'usuarios': usuarios
        })