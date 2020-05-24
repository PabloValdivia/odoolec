from odoo import fields, models, api


class SriErrorCodes(models.Model):
    _name = 'sri.errorcode'
    _description = 'SRI Error Code'

    code = fields.Char()
    name = fields.Char()
