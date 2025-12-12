import logging
import requests
from odoo import fields, models, _
from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class PaymentTransaction(models.Model):
    _inherit = 'payment.transaction'

    yape_transaction_id = fields.Char(string="ID Transacción Yape")
    yape_qr_code = fields.Text(string="Código QR Yape")

    def _get_specific_rendering_values(self, processing_values):
        res = super()._get_specific_rendering_values(processing_values)
        if self.provider_code != 'yape':
            return res

        # Generar QR para Yape
        qr_data = self._yape_generate_qr()
        res.update({
            'yape_qr_code': qr_data.get('qr_code'),
            'yape_transaction_id': qr_data.get('transaction_id'),
        })
        return res

    def _yape_generate_qr(self):
        """Genera código QR para pago con Yape"""
        api_url = self.provider_id._yape_get_api_url()
        
        payload = {
            'amount': self.amount,
            'currency': 'PEN',
            'reference': self.reference,
            'merchant_id': self.provider_id.yape_merchant_id,
            'callback_url': f"{self.get_base_url()}/payment/yape/callback"
        }
        
        headers = {
            'Authorization': f'Bearer {self._yape_get_access_token()}',
            'Content-Type': 'application/json'
        }
        
        try:
            response = requests.post(f"{api_url}/v1/qr/generate", json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
            
            self.yape_transaction_id = data.get('transaction_id')
            self.yape_qr_code = data.get('qr_code')
            
            return data
        except Exception as e:
            _logger.error(f"Error generando QR Yape: {e}")
            raise ValidationError(_("Error al generar código QR de Yape"))

    def _yape_get_access_token(self):
        """Obtiene token de acceso de Yape"""
        # Implementar autenticación OAuth2 con Yape
        return "token_placeholder"