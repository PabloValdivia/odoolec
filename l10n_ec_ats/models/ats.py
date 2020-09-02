from odoo import fields, models, api


class Ats(models.Model):
    _name = 'ats.ec'

    Company_ids = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('account.invoice'))
    month_date = fields.Date()
