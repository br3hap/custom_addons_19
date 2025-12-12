from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('yape', 'Yape')], ondelete={'yape': 'set default'}
    )
    
    # Campos específicos de Yape
    yape_client_id = fields.Char(
        string="Client ID",
        help="ID del cliente proporcionado por Yape",
        required_if_provider='yape'
    )
    yape_client_secret = fields.Char(
        string="Client Secret", 
        help="Clave secreta proporcionada por Yape",
        required_if_provider='yape'
    )
    yape_merchant_id = fields.Char(
        string="Merchant ID",
        help="ID del comercio en Yape",
        required_if_provider='yape'
    )
    yape_environment = fields.Selection([
        ('sandbox', 'Sandbox'),
        ('production', 'Producción')
    ], string="Entorno", default='sandbox', required_if_provider='yape')

    def _get_supported_currencies(self):
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'yape':
            supported_currencies = supported_currencies.filtered(lambda c: c.name == 'PEN')
        return supported_currencies

    def _yape_get_api_url(self):
        if self.yape_environment == 'sandbox':
            return 'https://sandbox-api.yape.com.pe'
        return 'https://api.yape.com.pe'