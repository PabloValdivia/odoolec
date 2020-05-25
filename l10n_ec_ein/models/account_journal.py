from odoo import fields, models, api


class Company(models.Model):
    _inherit = 'account.journal'

    is_electronic_document = fields.Boolean(default=False)
