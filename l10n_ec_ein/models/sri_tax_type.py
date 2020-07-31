from builtins import id

from odoo import fields, models, api


class TaxSriCode (models.Model):
    _name = 'lec.tax.code'
    _description = 'Sri Tax Code'

    code = fields.Char()
    name = fields.Char()
    rate_ids = fields.One2many('lec.tax.rate', 'tax_code_id')


class TaxSriRate (models.Model):
    _name = 'lec.tax.rate'
    _description = 'Sri Tax Rate'

    code = fields.Char('Code')
    name = fields.Char('Name')
    tax_code_id = fields.Many2one('lec.tax.code')


class Tax (models.Model):
    _inherit = 'account.tax'

    sri_code = fields.Many2one('lec.tax.code', 'code')
    sri_rate = fields.Many2one('lec.tax.rate', 'name')

