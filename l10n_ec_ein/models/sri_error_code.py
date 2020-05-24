from odoo import fields, models, api


class SriErrorCodes (models.Model):
    _name = 'sri.errorcode'

    code = fields.Char()
    name = fields.Char()
    


