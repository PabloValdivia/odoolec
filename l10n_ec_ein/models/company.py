from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'res.company'

    env_service = fields.Selection(
        [
            ('1', 'Test'),
            ('2', 'Production')
        ],
        string='Environment Type',
        required=True,
        default='1'
    )

    is_force_keep_accounting = fields.Selection(
        [
            ('SI', 'Yes'),
            ('NO', 'No')
        ],
        string = 'Keep Accounting',
        required='True',
        default='NO'
    )

    is_special_taxpayer = fields.Selection(
        [
            ('284', 'Yes'),
            ('000', 'No')
        ],
        string='Special TaxPayer',
        required='True',
        default='000'
    )




