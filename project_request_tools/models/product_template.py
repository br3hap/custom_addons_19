# -*- coding: utf-8 -*-
import logging

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    product_type_category = fields.Selection([
        ('tool', 'Herramienta'),
        ('epp', 'EPP'),
        ('material', 'Material'),
    ], string='Tipo de Producto')
