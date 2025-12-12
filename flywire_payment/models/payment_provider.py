# -*- coding: utf-8 -*-
from odoo import fields, models, api
import requests
import logging

_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(
        selection_add=[('flywire', 'Flywire')],
        ondelete={'flywire': 'set default'}
    )
    
    flywire_api_key = fields.Char(
        string='API Key',
        help='Flywire API Key'
    )
    
    flywire_secret_key = fields.Char(
        string='Secret Key',
        help='Flywire Secret Key'
    )
    
    flywire_environment = fields.Selection([
        ('demo', 'Demo (Sin API)'),
        ('sandbox', 'Sandbox'),
        ('production', 'Production')
    ], string='Environment', default='demo')
    
    @api.model
    def _get_demo_credentials(self):
        return {
            'api_key': 'demo_api_key_12345',
            'secret_key': 'demo_secret_key_67890'
        }

    def _get_supported_currencies(self):
        supported_currencies = super()._get_supported_currencies()
        if self.code == 'flywire':
            # Permitir todas las monedas para que aparezca siempre
            return supported_currencies
        return supported_currencies
    
    def _is_available_for(self, **kwargs):
        """Hacer que Flywire esté siempre disponible"""
        if self.code == 'flywire':
            return True
        return super()._is_available_for(**kwargs)

    def _flywire_get_api_url(self):
        if self.flywire_environment == 'production':
            return 'https://api.flywire.com'
        elif self.flywire_environment == 'sandbox':
            return 'https://api-platform-sandbox.flywire.com'
        return 'demo'  # Modo demo
    
    @api.model
    def _get_compatible_providers(self, *args, **kwargs):
        providers = super()._get_compatible_providers(*args, **kwargs)
        return providers