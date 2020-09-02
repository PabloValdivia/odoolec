from odoo import fields, models, api
from datetime import datetime

class Ats(models.Model):
    _name = 'ats.ec'

    Company_ids = fields.Many2one('res.company', default=lambda self: self.env['res.company']._company_default_get('account.invoice'))
    month = fields.Selection(
        [('1', 'Ene'), ('2', 'Feb'), ('3', 'Mar'), ('4', 'Abr'), ('5', 'May'), ('6', 'Jun'), ('7', 'Jul'),
                    ('8', 'Ago'), ('9', 'Sep'), ('10', 'Oct'), ('11', 'Nov'), ('12', 'Dic')]
    )
    year = fields.Integer('Year', required=True, default=datetime.today().strftime('%Y'))