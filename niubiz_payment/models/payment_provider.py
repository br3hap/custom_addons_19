from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('niubiz', 'Niubiz')], ondelete={'niubiz': 'set default'}
    )
    
    # Campos específicos de Niubiz
    niubiz_merchant_id = fields.Char(
        string="Merchant ID",
        help="ID del comercio proporcionado por Niubiz",
        required_if_provider='niubiz'
    )
    niubiz_access_key = fields.Char(
        string="Access Key",
        help="Clave de acceso proporcionada por Niubiz",
        required_if_provider='niubiz'
    )
    niubiz_secret_key = fields.Char(
        string="Secret Key", 
        help="Clave secreta proporcionada por Niubiz",
        required_if_provider='niubiz'
    )
    niubiz_environment = fields.Selection([
        ('test', 'Test'),
        ('live', 'Live')
    ], string="Entorno", default='test', required_if_provider='niubiz')

    def _get_supported_currencies(self):
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'niubiz':
            supported_currencies = supported_currencies.filtered(lambda c: c.name in ['PEN', 'USD'])
        return supported_currencies

    def _niubiz_get_api_url(self):
        if self.niubiz_environment == 'test':
            return 'https://apisandbox.vnforappstest.com'
        return 'https://apiprod.vnforapps.com'