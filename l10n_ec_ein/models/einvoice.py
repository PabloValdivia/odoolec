from odoo import fields, models, api


class Invoice(models.Model):
    _inherit = 'account.move'

    sri_authorization = fields.Many2one('sri.authorization')
    


