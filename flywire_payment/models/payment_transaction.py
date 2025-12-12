# -*- coding: utf-8 -*-
from odoo import fields, models, api, _
from odoo.exceptions import ValidationError
import requests
import logging

_logger = logging.getLogger(__name__)

class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    flywire_payment_id = fields.Char(string='Flywire Payment ID')

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'flywire':
            return res

        # Simulación de pago para demo
        rendering_values = {
            'api_url': 'demo',
            'payment_id': f'flywire_demo_{self.id}',
            'amount': self.amount,
            'currency': self.currency_id.name,
            'reference': self.reference,
        }
        return rendering_values

    def _flywire_simulate_payment(self):
        """Simular pago para demo"""
        self.flywire_payment_id = f'flywire_demo_{self.id}'
        return {
            'id': self.flywire_payment_id,
            'status': 'pending',
            'amount': self.amount,
            'currency': self.currency_id.name
        }

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code == 'flywire':
            self._flywire_process_notification(notification_data)

    def _flywire_process_notification(self, data):
        """Procesar notificación de Flywire"""
        status = data.get('status')
        
        if status == 'completed':
            self._set_done()
        elif status == 'failed':
            self._set_error('Payment failed')
        elif status == 'cancelled':
            self._set_canceled()