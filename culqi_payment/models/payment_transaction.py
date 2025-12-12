import logging
import requests
from odoo import _, fields, models
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    culqi_charge_id = fields.Char(string="Culqi Charge ID", readonly=True)
    culqi_token_id = fields.Char(string="Culqi Token ID", readonly=True)

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'culqi':
            return res

        rendering_values = {
            'culqi_public_key': self.provider_id.culqi_public_key,
            'amount_cents': int(self.amount * 100),
            'currency_code': self.currency_id.name,
            'reference': self.reference,
            'partner_email': self.partner_id.email or '',
            'return_url': self._get_landing_route(),
        }
        return rendering_values

    def _process_notification_data(self, notification_data):
        super()._process_notification_data(notification_data)
        if self.provider_code != 'culqi':
            return

        charge_id = notification_data.get('id')
        if charge_id:
            self.culqi_charge_id = charge_id
            
        # Verificar el estado del pago
        if notification_data.get('outcome', {}).get('type') == 'venta_exitosa':
            self._set_done()
        else:
            self._set_error("Pago rechazado por Culqi")

    def _culqi_create_charge(self, token_id):
        """Crear un cargo en Culqi usando el token"""
        url = f"{self.provider_id._culqi_get_api_url()}/v2/charges"
        
        headers = {
            'Authorization': f'Bearer {self.provider_id.culqi_secret_key}',
            'Content-Type': 'application/json'
        }
        
        data = {
            'amount': int(self.amount * 100),
            'currency_code': self.currency_id.name,
            'email': self.partner_id.email,
            'source_id': token_id,
            'description': f'Pago {self.reference}'
        }
        
        try:
            response = requests.post(url, json=data, headers=headers, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            _logger.error("Error al crear cargo en Culqi: %s", e)
            raise ValidationError(_("Error al procesar el pago con Culqi"))