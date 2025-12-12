import logging
import pprint
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class NiubizController(http.Controller):

    @http.route('/payment/niubiz/return', type='http', auth='public', methods=['GET', 'POST'], csrf=False)
    def niubiz_return(self, **kwargs):
        """Manejar el retorno desde Niubiz"""
        _logger.info("Retorno de Niubiz con datos: %s", pprint.pformat(kwargs))
        
        # Buscar la transacción por referencia
        reference = kwargs.get('reference')
        if reference:
            transaction = request.env['payment.transaction'].sudo().search([
                ('reference', '=', reference),
                ('provider_code', '=', 'niubiz')
            ], limit=1)
            
            if transaction:
                transaction._process_notification_data(kwargs)
                return request.redirect('/payment/status')
        
        return request.redirect('/payment/status')

    @http.route('/payment/niubiz/webhook', type='http', auth='public', methods=['POST'], csrf=False)
    def niubiz_webhook(self, **kwargs):
        """Webhook para notificaciones de Niubiz"""
        _logger.info("Webhook de Niubiz con datos: %s", pprint.pformat(kwargs))
        
        # Procesar la notificación
        reference = kwargs.get('reference')
        if reference:
            transaction = request.env['payment.transaction'].sudo().search([
                ('reference', '=', reference),
                ('provider_code', '=', 'niubiz')
            ], limit=1)
            
            if transaction:
                transaction._process_notification_data(kwargs)
        
        return 'OK'