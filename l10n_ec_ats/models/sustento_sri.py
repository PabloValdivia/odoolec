from odoo import fields, models, api


class SustentsTax(models.Model):
    _name = 'sustents.tax'

    name = fields.Char()
    code = fields.Char()
    description = fields.Char()
    move_ids = fields.One2many('account.move', 'sustento_id')
