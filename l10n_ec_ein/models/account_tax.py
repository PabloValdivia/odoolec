from odoo import fields, models, api


class Tax(models.Model):
    _inherit = 'account.tax'

    sri_tax_type = fields.Selection(
        [
            ('vat', 'Iva 12'),
            ('vat0', 'Iva 0'),
            ('ice', 'ICE')
        ]
    )



