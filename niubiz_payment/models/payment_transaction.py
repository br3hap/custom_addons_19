import logging
import requests
import base64
import json
from datetime import datetime
from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    niubiz_session_token = fields.Char(string="Niubiz Session Token", readonly=True)
    niubiz_purchase_number = fields.Char(string="Niubiz Purchase Number", readonly=True)
    niubiz_transaction_id = fields.Char(string="Niubiz Transaction ID", readonly=True)

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'niubiz':
            return res

        # Generar session token
        session_token = self._niubiz_get_session_token()
        
        rendering_values = {
            'niubiz_merchant_id': self.provider_id.niubiz_merchant_id,
            'session_token': session_token,
            'amount': self.amount,
            'currency_code': self.currency_id.name,
            'reference': self.reference,
            'partner_email': self.partner_id.email or '',
            'return_url': self._get_landing_route(),
            'api_url': self.provider_id._niubiz_get_api_url(),
        }
        return rendering_values

    def _niubiz_get_session_token(self):
        """Obtener token de sesión de Niubiz"""
        url = f"{self.provider_id._niubiz_get_api_url()}/api.security/v1/security"
        
        # Crear autenticación básica
        credentials = f"{self.provider_id.niubiz_access_key}:{self.provider_id.niubiz_secret_key}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        
        headers = {
            'Authorization': f'Basic {encoded_credentials}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(url, headers=headers, timeout=30)
            response.raise_for_status()
            token = response.text.strip('"')
            self.niubiz_session_token = token
            return token
        except requests.exceptions.RequestException as e:
            _logger.error("Error al obtener token de Niubiz: %s", e)
            raise ValidationError(_("Error al conectar con Niubiz"))

    def _niubiz_authorize_transaction(self, purchase_number, transaction_token):
        """Autorizar transacción en Niubiz"""
        url = f"{self.provider_id._niubiz_get_api_url()}/api.authorization/v3/authorization/ecommerce/{self.provider_id.niubiz_merchant_id}"
        
        headers = {
            'Authorization': f'{self.niubiz_session_token}',
            'Content-Type': 'application/json'
        }
        
        data = {
            "channel": "web",
            "captureType": "manual",
            "countable": True,
            "order": {
                "tokenId": transaction_token,
                "purchaseNumber": purchase_number,
                "amount": self.amount,
                "currency": self.currency_id.name
            }
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _logger.error("Error al autorizar transacción en Niubiz: %s", e)
            raise ValidationError(_("Error al procesar el pago con Niubiz"))

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'niubiz':
            return

        transaction_id = notification_data.get('transactionUuid')
        if transaction_id:
            self.niubiz_transaction_id = transaction_id
            
        # Verificar el estado del pago
        if notification_data.get('dataMap', {}).get('ACTION_CODE') == '000':
            self._set_done()
        else:
            error_msg = notification_data.get('dataMap', {}).get('ACTION_DESCRIPTION', 'Pago rechazado')
            self._set_error(f"Pago rechazado por Niubiz: {error_msg}")