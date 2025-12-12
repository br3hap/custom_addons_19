# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import logging

_logger = logging.getLogger(__name__)

class FlywireController(http.Controller):

    @http.route('/payment/flywire/return', type='http', auth='public', csrf=False)
    def flywire_return(self, **kwargs):
        """Manejo del retorno desde Flywire"""
        _logger.info('Flywire return: %s', kwargs)
        
        payment_id = kwargs.get('payment_id')
        if payment_id:
            transaction = request.env['payment.transaction'].sudo().search([
                ('flywire_payment_id', '=', payment_id)
            ], limit=1)
            
            if transaction:
                transaction._process_notification_data(kwargs)
                return request.redirect('/payment/status')
        
        return request.redirect('/shop/payment')

    @http.route('/payment/flywire/cancel', type='http', auth='public', csrf=False)
    def flywire_cancel(self, **kwargs):
        """Manejo de cancelación desde Flywire"""
        _logger.info('Flywire cancel: %s', kwargs)
        return request.redirect('/shop/payment')

    @http.route('/payment/flywire/webhook', type='http', auth='public', csrf=False, methods=['POST'])
    def flywire_webhook(self, **kwargs):
        """Webhook para notificaciones de Flywire"""
        _logger.info('Flywire webhook: %s', kwargs)
        
        payment_id = kwargs.get('payment_id')
        if payment_id:
            transaction = request.env['payment.transaction'].sudo().search([
                ('flywire_payment_id', '=', payment_id)
            ], limit=1)
            
            if transaction:
                transaction._process_notification_data(kwargs)
        
        return 'OK'