import logging
import pprint
from odoo import http
from odoo.http import request

_logger = logging.getLogger(__name__)


class CulqiController(http.Controller):

    @http.route('/payment/culqi/return', type='http', auth='public', csrf=False, save_session=False)
    def culqi_return_from_checkout(self, **data):
        """Manejar el retorno desde Culqi"""
        _logger.info("Retorno de Culqi con datos: %s", pprint.pformat(data))
        
        # Buscar la transacción
        tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
            'culqi', data
        )
        
        # Procesar la notificación
        tx_sudo._process_notification_data(data)
        
        return request.redirect('/payment/status')

    @http.route('/payment/culqi/webhook', type='http', auth='public', csrf=False, save_session=False)
    def culqi_webhook(self, **data):
        """Webhook para notificaciones de Culqi"""
        _logger.info("Webhook de Culqi recibido: %s", pprint.pformat(data))
        
        try:
            # Buscar la transacción
            tx_sudo = request.env['payment.transaction'].sudo()._get_tx_from_notification_data(
                'culqi', data
            )
            
            # Procesar la notificación
            tx_sudo._process_notification_data(data)
            
            return 'OK'
        except Exception as e:
            _logger.error("Error procesando webhook de Culqi: %s", e)
            return 'ERROR'

    @http.route('/payment/culqi/process', type='json', auth='public', csrf=False)
    def culqi_process_payment(self, **kwargs):
        """Procesar el pago con token de Culqi"""
        token_id = kwargs.get('token_id')
        tx_reference = kwargs.get('reference')
        
        if not token_id or not tx_reference:
            return {'error': 'Datos incompletos'}
        
        try:
            # Buscar la transacción
            tx_sudo = request.env['payment.transaction'].sudo().search([
                ('reference', '=', tx_reference)
            ], limit=1)
            
            if not tx_sudo:
                return {'error': 'Transacción no encontrada'}
            
            # Crear el cargo en Culqi
            charge_data = tx_sudo._culqi_create_charge(token_id)
            
            # Procesar la respuesta
            tx_sudo._process_notification_data(charge_data)
            
            return {'success': True, 'charge_id': charge_data.get('id')}
            
        except Exception as e:
            _logger.error("Error procesando pago Culqi: %s", e)
            return {'error': str(e)}