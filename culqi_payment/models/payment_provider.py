from odoo import fields, models


class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('culqi', 'Culqi')], ondelete={'culqi': 'set default'}
    )
    
    # Campos específicos de Culqi
    culqi_public_key = fields.Char(
        string="Public Key",
        help="Llave pública proporcionada por Culqi",
        required_if_provider='culqi'
    )
    culqi_secret_key = fields.Char(
        string="Secret Key", 
        help="Llave secreta proporcionada por Culqi",
        required_if_provider='culqi'
    )
    culqi_environment = fields.Selection([
        ('test', 'Test'),
        ('live', 'Live')
    ], string="Entorno", default='test', required_if_provider='culqi')

    def _get_supported_currencies(self):
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'culqi':
            supported_currencies = supported_currencies.filtered(lambda c: c.name in ['PEN', 'USD'])
        return supported_currencies

    def _culqi_get_api_url(self):
        if self.culqi_environment == 'test':
            return 'https://api.culqi.com'
        return 'https://api.culqi.com'